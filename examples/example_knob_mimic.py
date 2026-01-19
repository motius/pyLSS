# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)
# Description: Moves one LSS using the position of a second LSS.
# One servo acts as an input (limp mode) and the other mimics its position.

import time
import serial
from pylss import LSS
from pylss.constants import DEFAULT_BAUD

# Constants
# PORT = "/dev/ttyUSB0"  # For Linux/Unix platforms
PORT = "COM230"  # For Windows platforms
BAUD_RATE = DEFAULT_BAUD

# Hysteresis threshold in tenths of degrees (±2 tenths = ±0.2 degrees)
POSITION_THRESHOLD = 2


def main() -> None:
    """Use one servo as input (knob) to control another servo (output)."""
    # Create and open a serial port
    bus = serial.Serial(PORT, BAUD_RATE, timeout=0.1)

    try:
        # Create two LSS objects: one for output (ID=0), one for input (ID=1)
        output_servo = LSS(0, bus)
        input_servo = LSS(1, bus)

        # Initialize output servo to position 0.0 degrees
        print("Initializing output servo to 0 degrees...")
        output_servo.move_deg(0.0)

        # Wait for it to get there
        time.sleep(2)

        # Configure output servo for smooth following
        print("Configuring output servo...")
        output_servo.set_angular_stiffness(4)
        output_servo.set_max_speed_rpm(15)

        # Make input servo limp (no active resistance, acts as a knob)
        print("Setting input servo to limp mode...")
        input_servo.limp()

        print("\nMimicking input servo position. Press Ctrl+C to stop.")
        print("Manually move the input servo to control the output servo.\n")

        # Track last position to implement hysteresis
        last_position_deg = 0.0

        # Reproduce position of input_servo on output_servo
        while True:
            # Wait ~20 ms before sending another command (update at most 50 times per second)
            time.sleep(0.02)

            # Get position from input servo
            current_position_deg = input_servo.get_position_deg()

            # Check if position changed enough to warrant sending (hysteresis of ±0.2 degrees)
            position_delta = abs(current_position_deg - last_position_deg)

            if position_delta > (POSITION_THRESHOLD / 10):
                # Send position to output servo and display
                print(f"Input @ {current_position_deg:6.1f}° → Output")
                output_servo.move_deg(current_position_deg)
                last_position_deg = current_position_deg

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        # Clean up
        bus.close()


if __name__ == "__main__":
    main()
