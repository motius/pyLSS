# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)
# Description: Basic example of reading values from the LSS and displaying
# them in the terminal.

import time
import serial
from pylss import LSS
from pylss.constants import DEFAULT_BAUD

# Constants
# PORT = "/dev/ttyUSB0"  # For Linux/Unix platforms
PORT = "COM230"  # For Windows platforms
BAUD_RATE = DEFAULT_BAUD


def main() -> None:
    """Query and display servo telemetry continuously."""
    # Create and open a serial port
    bus = serial.Serial(PORT, BAUD_RATE, timeout=0.1)

    try:
        # Create an LSS object for servo ID 0
        servo = LSS(0, bus)

        print("Querying LSS telemetry. Press Ctrl+C to stop.\n")

        while True:
            # Get the values from LSS
            print("Querying LSS...")

            position = servo.get_position_deg()
            rpm = servo.get_speed_rpm()
            current = servo.get_current()
            voltage = servo.get_voltage()
            temperature = servo.get_temperature()

            # Display the values in terminal
            print("\n---- Telemetry ----")
            print(f"Position:      {position:7.1f} degrees")
            print(f"Speed:         {rpm:7d} rpm")
            print(f"Current:       {current:7d} mA")
            print(f"Voltage:       {voltage:7d} mV ({voltage / 1000:.1f} V)")
            print(f"Temperature:   {temperature / 10:7.1f} °C")
            print()

            # Wait 1 second
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        # Clean up
        bus.close()


if __name__ == "__main__":
    main()
