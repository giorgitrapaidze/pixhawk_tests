# Pixhawk Thruster Tests

This repository contains Python scripts to test underwater thruster configurations using a Pixhawk flight controller. It includes scripts for testing a single thruster as well as synchronized dual-thruster setups.

## Prerequisites

Before running the scripts, ensure you have:
* **Python 3.8+** installed on your system.
* A Pixhawk flight controller connected via USB or telemetry.
* Thrusters correctly wired to the Pixhawk's PWM/servo outputs.

---

## Installation & Setup

Follow these steps to set up your local environment and install the required dependencies.

### 1. Clone the Repository

```bash
git clone git@github.com:giorgitrapaidze/pixhawk_tests.git
cd pixhawk_tests
```

### 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies cleanly.

* **Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

* **Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required packages (such as `pymavlink`):

```bash
pip install -r requirements.txt
```

---

## Usage & Tests

⚠️ **Safety Warning:** Ensure your vehicle/thrusters are securely mounted or placed in a safe testing environment (e.g., test tank or dry setup with propellers removed) before sending PWM commands.

### 1. Single Thruster Test

To test the initialization and basic spin of a single thruster, run:

```bash
python test_thruster.py
```

**What it does:** Connects to the Pixhawk, arms the system, and sends step-by-step PWM signals to a single designated channel to verify directional control and thrust scaling.

### 2. Dual Thruster Test

To test synchronized movements, differential steering, or dual thrust configurations, run:

```bash
python test_two_thruster.py
```

**What it does:** Arms the Pixhawk and sends simultaneous control commands to two thruster channels to verify they respond correctly in tandem.

---

## Repository Structure

```
├── .gitignore               # Ensures .venv, caches, etc., aren't tracked
├── requirements.txt         # Python dependencies (PyMavlink, etc.)
├── README.md                # Project documentation
├── test_thruster.py         # Script for single thruster validation
└── test_two_thruster.py     # Script for dual thruster validation
```