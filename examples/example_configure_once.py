# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)
# Description: Example of all the possible configurations for a LSS.

import time
import serial
from pylss import LSS
from pylss.constants import (
    DEFAULT_BAUD,
    LedColor,
    GyreDirection,  # noqa: F401 used in commented examples
    SetType,  # noqa: F401 used in commented examples
)

# Constants
PORT = "/dev/ttyUSB0"  # For Linux/Unix platforms
# PORT = "COM230"  # For Windows platforms
BAUD_RATE = DEFAULT_BAUD


def main() -> None:
    """Configure an LSS servo and demonstrate LED color changes."""
    # Create and open a serial port
    bus = serial.Serial(PORT, BAUD_RATE, timeout=0.1)

    try:
        # Create an LSS object for servo ID 0
        servo = LSS(0, bus)

        # Uncomment any configurations that you wish to activate
        # You can see above each configuration a link to its description in the Lynxmotion wiki
        # Note: If you change a configuration to the same value that is already set,
        #       the LSS will ignore the operation since the value is not changed.

        # *** Basic configurations ***
        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H6.OriginOffsetAction28O29
        # servo.set_origin_offset_deg(0.0, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H7.AngularRange28AR29
        # servo.set_angular_range_deg(180.0, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H12.MaxSpeedinDegrees28SD29
        # servo.set_max_speed_deg_per_sec(60.0, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H13.MaxSpeedinRPM28SR29
        # servo.set_max_speed_rpm(100, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H14.LEDColor28LED29
        # Options are:
        # LedColor.BLACK = 0
        # LedColor.RED = 1
        # LedColor.GREEN = 2
        # LedColor.BLUE = 3
        # LedColor.YELLOW = 4
        # LedColor.CYAN = 5
        # LedColor.MAGENTA = 6
        # LedColor.WHITE = 7
        # servo.set_color_led(LedColor.BLACK, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H15.GyreRotationDirection28G29
        # Options are:
        # GyreDirection.CLOCKWISE = 1
        # GyreDirection.COUNTER_CLOCKWISE = -1
        # servo.set_gyre(GyreDirection.CLOCKWISE, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#H19.FirstA0Position28Degrees29
        # servo.set_first_position_deg(0.0)
        # servo.clear_first_position()

        # *** Advanced configurations ***
        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#HA1.AngularStiffness28AS29
        # servo.set_angular_stiffness(0, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#HA2.AngularHoldingStiffness28AH29
        # servo.set_angular_holding_stiffness(4, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#HA3:AngularAcceleration28AA29
        # servo.set_angular_acceleration(100, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#HA4:AngularDeceleration28AD29
        # servo.set_angular_deceleration(100, SetType.CONFIG)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#HA5:MotionControl28EM29
        # servo.set_motion_control_enabled(1)

        # https://www.robotshop.com/info/wiki/lynxmotion/view/lynxmotion-smart-servo/lss-communication-protocol/#HA6.ConfigureLEDBlinking28CLB29
        # Options are an arithmetic addition of the following values:
        # Limp       1
        # Holding    2
        # Accelerating   4
        # Decelerating   8
        # Free       16
        # Traveling 32
        # Therefore, 0 = no blinking and 63 = always blinking
        # servo.set_blinking_led(0)

        # Reset motor to complete change of configurations
        servo.reset()

        # Wait for reboot
        time.sleep(2)

        print("Cycling through LED colors. Press Ctrl+C to stop.")

        # Loop through each of the 8 LED colors
        while True:
            for color in LedColor:
                # Set the color (session) of the LSS
                servo.set_color_led(color)
                print(f"LED Color: {color.name}")
                # Wait 1 second per color change
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        # Clean up
        bus.close()


if __name__ == "__main__":
    main()
