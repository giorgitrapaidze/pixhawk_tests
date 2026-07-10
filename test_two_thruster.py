import time
from pymavlink import mavutil

def run_unbroken_stream():
    port = '/dev/ttyACM0'
    print(f"Connecting to Pixhawk on {port}...")
    master = mavutil.mavlink_connection(port, baud=115200, source_system=255, source_component=0)
    
    master.wait_heartbeat()
    print("Connected!")

    # Unified function to feed both GCS heartbeat and neutral RC overrides
    def feed_watchdog(target_pwm=1500):
        # 1. Send the mandatory GCS heartbeat
        master.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_GCS,
            mavutil.mavlink.MAV_AUTOPILOT_INVALID,
            0, 0, 0
        )
        # 2. Keep the RC channel override stream hot (Channel 5 is index 4)
        rc_values = [65535] * 8
        rc_values[4] = target_pwm
        master.mav.rc_channels_override_send(
            master.target_system, master.target_component, *rc_values
        )

    # 1. Establish an active data baseline before doing anything
    print("Pre-streaming neutral signal to satisfy safety watchdogs...")
    for _ in range(20):
        feed_watchdog(1500)
        time.sleep(0.05)  # High-frequency 20Hz stream

    # 2. Force Set Flight Mode to MANUAL
    print("Setting mode to MANUAL...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
        1, 0, 0, 0, 0, 0, 0
    )
    
    # Maintain stream briefly after mode switch
    for _ in range(10):
        feed_watchdog(1500)
        time.sleep(0.05)

    # 3. ARM WHILE MAINTAINING STREAM
    print("Arming vehicle...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
        1, 21196, 0, 0, 0, 0, 0
    )

    # Keep streaming neutral for 1 second right after arming so it stays armed
    print("Holding ARM state steady...")
    start_hold = time.time()
    while time.time() - start_hold < 1.0:
        feed_watchdog(1500)
        time.sleep(0.05)

    # 4. EXECUTE SPIN (Transition the active stream to target speed)
    print("Streaming active throttle (1620 PWM)...")
    start_spin = time.time()
    while time.time() - start_spin < 3.0:
        feed_watchdog(1620)  # Pumping forward throttle actively at 20Hz
        time.sleep(0.05)

    # 5. GRACEFUL SHUTDOWN
    print("Bringing motor to stop and disarming...")
    for _ in range(10):
        feed_watchdog(1500)
        time.sleep(0.05)

    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
        0, 0, 0, 0, 0, 0, 0
    )
    print("Sequence clean. Complete.")

if __name__ == "__main__":
    run_unbroken_stream()