# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)
# Description: Basic example of the LSS moving back and forth.

import time
import serial
from pylss import LSS
from pylss.constants import DEFAULT_BAUD

# Constants
# PORT = "/dev/ttyUSB0"  # For Linux/Unix platforms
PORT = "COM230"  # For Windows platforms
BAUD_RATE = DEFAULT_BAUD


def main() -> None:
    """Move the servo back and forth between -180 and +180 degrees."""
    # Create and open a serial port
    bus = serial.Serial(PORT, BAUD_RATE, timeout=0.1)

    try:
        # Create an LSS object for servo ID 0
        servo = LSS(0, bus)

        # Initialize LSS to position 0.0 degrees
        servo.move_deg(0.0)
        print("Moving to 0 degrees...")

        # Wait for it to get there
        time.sleep(2)

        print("Starting sweep. Press Ctrl+C to stop.")

        # Loop between -180.0 deg and 180.0 deg, pausing 2 seconds between moves
        while True:
            # Send LSS to half a turn counter-clockwise from zero (assumes gyre = 1)
            print("Moving to -180 degrees")
            servo.move_deg(-180.0)

            # Wait for two seconds
            time.sleep(2)

            # Send LSS to half a turn clockwise from zero (assumes gyre = 1)
            print("Moving to +180 degrees")
            servo.move_deg(180.0)

            # Wait for two seconds
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        # Clean up
        bus.close()


if __name__ == "__main__":
    main()
