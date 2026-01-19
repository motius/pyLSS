# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)

from enum import IntEnum, StrEnum

# List of constants

# Bus communication
DEFAULT_BAUD = 115200
# Command Length
# example: #999XXXX-2147483648\r Adding 1 for end string char (\0)
MAX_TOTAL_COMMAND_LENGTH = 30 + 1
TIMEOUT_MS = 100
COMMAND_START = "#"
COMMAND_REPLY_START = "*"
COMMAND_END = "\r"
FIRST_POSITION_DISABLED = "DIS"


# LSS ID constants
class ServoID(IntEnum):
    """Servo ID range constants"""

    DEFAULT = 0
    MIN = 0
    MAX = 250
    MODE_255 = 255
    BROADCAST = 254


# Read/write status
class ComStatus(IntEnum):
    """Communication status codes"""

    IDLE = 0
    READ_SUCCESS = 1
    READ_TIMEOUT = 2
    READ_WRONG_ID = 3
    READ_WRONG_IDENTIFIER = 4
    READ_WRONG_FORMAT = 5
    READ_NO_BUS = 6
    READ_UNKNOWN = 7
    WRITE_SUCCESS = 8
    WRITE_NO_BUS = 9
    WRITE_UNKNOWN = 10


# LSS status
class Status(IntEnum):
    """Servo status codes"""

    UNKNOWN = 0
    LIMP = 1
    FREE_MOVING = 2
    ACCELERATING = 3
    TRAVELING = 4
    DECELERATING = 5
    HOLDING = 6
    OUTSIDE_LIMITS = 7
    STUCK = 8  # cannot move at current speed setting
    BLOCKED = 9  # same as stuck but reached maximum duty and still can't move
    SAFE_MODE = 10
    LAST = 11


# LSS models
class Model(IntEnum):
    """Servo model types"""

    HIGH_TORQUE = 0
    STANDARD = 1
    HIGH_SPEED = 2
    UNKNOWN = 3


# Model string constants
class ModelString(StrEnum):
    """Servo model string identifiers"""

    HT1 = "LSS-HT1"
    ST1 = "LSS-ST1"
    HS1 = "LSS-HS1"


# Parameter for query
class QueryType(IntEnum):
    """Query parameter types"""

    SESSION = 0
    CONFIG = 1
    INSTANTANEOUS_SPEED = 2
    TARGET_TRAVEL_SPEED = 3


# Parameter for setter
class SetType(IntEnum):
    """Setter parameter types"""

    SESSION = 0
    CONFIG = 1


# Parameter for Serial/RC mode change
class Mode(IntEnum):
    """Operating modes"""

    SERIAL = 0
    POSITION_RC = 1
    WHEEL_RC = 2


# Parameter for gyre direction
class GyreDirection(IntEnum):
    """Rotation direction"""

    CLOCKWISE = 1
    COUNTER_CLOCKWISE = -1


# LED colors
class LedColor(IntEnum):
    """LED color codes"""

    BLACK = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    CYAN = 5
    MAGENTA = 6
    WHITE = 7


# Commands - actions
class Action(StrEnum):
    """Action command strings"""

    RESET = "RESET"
    LIMP = "L"
    HOLD = "H"
    PARAMETER_TIME = "T"
    PARAMETER_SPEED = "S"
    MOVE = "D"
    MOVE_RELATIVE = "MD"
    WHEEL = "WD"
    WHEEL_RPM = "WR"
    ORIGIN_OFFSET = "O"
    ANGULAR_RANGE = "AR"
    MAX_SPEED = "SD"
    MAX_SPEED_RPM = "SR"
    COLOR_LED = "LED"
    GYRE_DIRECTION = "G"
    ANGULAR_STIFFNESS = "AS"
    ANGULAR_HOLDING_STIFFNESS = "AH"
    ANGULAR_ACCELERATION = "AA"
    ANGULAR_DECELERATION = "AD"
    ENABLE_MOTION_CONTROL = "EM"


# Commands - queries
class Query(StrEnum):
    """Query command strings"""

    STATUS = "Q"
    ORIGIN_OFFSET = "QO"
    ANGULAR_RANGE = "QAR"
    POSITION_PULSE = "QP"
    POSITION = "QD"
    SPEED = "QWD"
    SPEED_RPM = "QWR"
    SPEED_PULSE = "QS"
    MAX_SPEED = "QSD"
    MAX_SPEED_RPM = "QSR"
    COLOR_LED = "QLED"
    GYRE = "QG"
    ID = "QID"
    BAUD = "QB"
    FIRST_POSITION = "QFD"
    MODEL_STRING = "QMS"
    SERIAL_NUMBER = "QN"
    FIRMWARE_VERSION = "QF"
    VOLTAGE = "QV"
    TEMPERATURE = "QT"
    CURRENT = "QC"
    ANGULAR_STIFFNESS = "QAS"
    ANGULAR_HOLDING_STIFFNESS = "QAH"
    ANGULAR_ACCELERATION = "QAA"
    ANGULAR_DECELERATION = "QAD"
    ENABLE_MOTION_CONTROL = "QEM"
    BLINKING_LED = "QLB"


# Commands - configurations
class Config(StrEnum):
    """Configuration command strings"""

    ID = "CID"
    BAUD = "CB"
    ORIGIN_OFFSET = "CO"
    ANGULAR_RANGE = "CAR"
    MAX_SPEED = "CSD"
    MAX_SPEED_RPM = "CSR"
    COLOR_LED = "CLED"
    GYRE_DIRECTION = "CG"
    FIRST_POSITION = "CFD"
    MODE = "CRC"
    ANGULAR_STIFFNESS = "CAS"
    ANGULAR_HOLDING_STIFFNESS = "CAH"
    ANGULAR_ACCELERATION = "CAA"
    ANGULAR_DECELERATION = "CAD"
    BLINKING_LED = "CLB"
