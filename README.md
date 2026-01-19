# Lynxmotion Smart Servo (LSS) Python Library

Official Lynxmotion Smart Servo (LSS) libraries for Python

Read more about the LSS on our [wiki](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v2/lynxmotion-smart-servo/).

If you want more details about the LSS protocol, go [here](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v2/lynxmotion-smart-servo/lss-communication-protocol/).

To configure your LSS easily, we recommend you try out the [LSS Config](https://www.robotshop.com/products/lynxmotion-lss-configuration-software?qd=e28060e7570ef850c9f4421ea1dccf99).
More details about it [on the wiki](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v2/lynxmotion-smart-servo/lss-configuration-software/).

Purchase any LSS model on and accessories at [RobotShop](https://www.robotshop.com)!

Check out blogs, tutorials and post questions on the RobotShop [community site](https://www.robotshop.com/community/).

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. If you don't have uv installed:

```bash
# Install uv (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### Install the library

```bash
# Clone the repository
git clone https://github.com/Robotics-Technology/PyLSS.git
cd PyLSS

# Install dependencies
uv sync

# Or install in development mode with all dependencies
uv sync --all-groups
```

### Using the library in your project

```python
import serial
from pylss import LSS

# Create and open a serial connection
bus = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)

# Create an LSS servo controller for servo ID 5
servo = LSS(5, bus)

# Move to 45 degrees
servo.move_deg(45.0)

# Get current position
position = servo.get_position_deg()
print(f"Current position: {position}°")

# Get servo information
model = servo.get_model()
voltage = servo.get_voltage()
temperature = servo.get_temperature()

print(f"Model: {model}")
print(f"Voltage: {voltage}mV")
print(f"Temperature: {temperature/10}°C")

# Clean up
bus.close()
```

## Running Examples

The repository includes several example scripts in the [examples](examples/) directory:

## Testing

The library includes a comprehensive test suite using pytest with mocked serial communication, so no hardware is required to run tests.

### Run all tests

```bash
# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ --cov=pylss

# Run specific test class
uv run pytest tests/test.py::TestLSSActionMethods -v
```

All tests use mocked serial objects, making them fast and reliable without requiring physical hardware.
