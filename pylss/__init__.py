# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)

"""Lynxmotion Smart Servo (LSS) Python Library.

This library provides an interface to control Lynxmotion Smart Servo (LSS)
actuators via serial communication.

Example:
    >>> import serial
    >>> from pylss import LSS
    >>>
    >>> bus = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
    >>> servo = LSS(5, bus)
    >>> servo.move_deg(45.0)
    >>> position = servo.get_position_deg()
    >>> bus.close()
"""

from .lss import LSS
from .constants import (
    DEFAULT_BAUD,
    TIMEOUT_MS,
    Action,
    Query,
    Config,
    QueryType,
    SetType,
    Mode,
    Status,
    Model,
    ModelString,
    ServoID,
    ComStatus,
    GyreDirection,
    LedColor,
)

__version__ = "0.1.0"
__author__ = "Sebastien Parent-Charette, Sebastian Plamauer"
__license__ = "LGPL-3.0-or-later"

__all__ = [
    # Main class
    "LSS",
    # Constants
    "DEFAULT_BAUD",
    "TIMEOUT_MS",
    # Command enums
    "Action",
    "Query",
    "Config",
    # Parameter types
    "QueryType",
    "SetType",
    "Mode",
    # Status and identification
    "Status",
    "Model",
    "ModelString",
    "ServoID",
    "ComStatus",
    # Configuration
    "GyreDirection",
    "LedColor",
]
