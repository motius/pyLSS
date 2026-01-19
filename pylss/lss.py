# Author: Sebastien Parent-Charette (support@robotshop.com)
# License: LGPL-3.0 (GNU Lesser General Public License version 3)

import re
import serial

from .constants import (
    TIMEOUT_MS,
    COMMAND_START,
    COMMAND_REPLY_START,
    COMMAND_END,
    Action,
    Query,
    Config,
    QueryType,
    SetType,
)


class LSS:
    """Lynxmotion Smart Servo (LSS) controller class.

    This class provides an interface to control LSS smart servos via serial communication.
    Each instance represents a single servo on a shared serial bus.
    """

    def __init__(self, servo_id: int, bus: serial.Serial) -> None:
        """Initialize an LSS servo controller.

        Args:
            servo_id: The ID of the servo to control (0-254)
            bus: Serial connection to the servo bus
        """
        self.servo_id = servo_id
        self.bus = bus
        if self.bus:
            self.bus.timeout = TIMEOUT_MS

    def __del__(self) -> None:
        """Close the serial connection when the object is deleted."""
        if hasattr(self, "bus") and self.bus and self.bus.is_open:
            self.bus.close()

    def _write(self, cmd: str, param: int | str | None = None) -> None:
        """Write a command to the servo.

        Args:
            cmd: Command string to send
            param: Optional parameter value

        Raises:
            Exception: If serial bus is not available or not open
        """
        if not self.bus or not self.bus.is_open:
            raise Exception("Serial bus is not available or not open")

        if param is None:
            message = f"{COMMAND_START}{self.servo_id}{cmd}{COMMAND_END}"
        else:
            message = f"{COMMAND_START}{self.servo_id}{cmd}{param}{COMMAND_END}"

        self.bus.write(message.encode())

    def _read_int(self, cmd: str) -> int:
        """Read an integer response from the servo.

        Args:
            cmd: Command string that was sent

        Returns:
            Integer value from servo

        Raises:
            Exception: If serial bus is not available, timeout occurs, or response is invalid
        """
        if not self.bus or not self.bus.is_open:
            raise Exception("Serial bus is not available or not open")

        try:
            # Find start of packet
            c = self.bus.read()
            while c.decode("utf-8") != COMMAND_REPLY_START:
                c = self.bus.read()
                if c.decode("utf-8") == "":
                    raise Exception(f"Timeout waiting for response to command '{cmd}'")

            # Read until end marker
            data = self.bus.read_until(COMMAND_END.encode("utf-8"))

            # Parse response: ID + Command + Value
            matches = re.match(
                r"(\d{1,3})([A-Z]{1,4})(-?\d{1,18})", data.decode("utf-8"), re.I
            )

            if not matches:
                raise Exception(
                    f"Malformed response for command '{cmd}': {data.decode('utf-8')}"
                )

            read_id, read_ident, read_value = matches.groups()

            # Verify response matches request
            if read_id != str(self.servo_id):
                raise Exception(
                    f"Response from wrong servo ID: expected {self.servo_id}, got {read_id}"
                )

            if read_ident != cmd:
                raise Exception(
                    f"Response command mismatch: expected '{cmd}', got '{read_ident}'"
                )

            return int(read_value)

        except Exception as e:
            if (
                "Serial bus" in str(e)
                or "Timeout" in str(e)
                or "Malformed" in str(e)
                or "Response" in str(e)
            ):
                raise
            raise Exception(f"Communication error reading command '{cmd}': {str(e)}")

    def _read_str(self, cmd: str, num_chars: int) -> str:
        """Read a string response from the servo.

        Args:
            cmd: Command string that was sent
            num_chars: Expected number of characters in response

        Returns:
            String value from servo

        Raises:
            Exception: If serial bus is not available, timeout occurs, or response is invalid
        """
        if not self.bus or not self.bus.is_open:
            raise Exception("Serial bus is not available or not open")

        try:
            # Find start of packet
            c = self.bus.read()
            while c.decode("utf-8") != COMMAND_REPLY_START:
                c = self.bus.read()
                if c.decode("utf-8") == "":
                    raise Exception(f"Timeout waiting for response to command '{cmd}'")

            # Read until end marker
            data = self.bus.read_until(COMMAND_END.encode("utf-8"))[:-1]

            # Parse response: ID + Command + Value
            matches = re.match(
                rf"(\d{{1,3}})([A-Z]{{1,4}})(.{{{num_chars}}})",
                data.decode("utf-8"),
                re.I,
            )

            if not matches:
                raise Exception(
                    f"Malformed response for command '{cmd}': {data.decode('utf-8')}"
                )

            read_id, read_ident, read_value = matches.groups()

            # Verify response matches request
            if read_id != str(self.servo_id):
                raise Exception(
                    f"Response from wrong servo ID: expected {self.servo_id}, got {read_id}"
                )

            if read_ident != cmd:
                raise Exception(
                    f"Response command mismatch: expected '{cmd}', got '{read_ident}'"
                )

            return read_value

        except Exception as e:
            if (
                "Serial bus" in str(e)
                or "Timeout" in str(e)
                or "Malformed" in str(e)
                or "Response" in str(e)
            ):
                raise
            raise Exception(f"Communication error reading command '{cmd}': {str(e)}")

    # Action methods

    def reset(self) -> None:
        """Reset the servo."""
        self._write(Action.RESET)

    def limp(self) -> None:
        """Put the servo in limp mode (no torque)."""
        self._write(Action.LIMP)

    def hold(self) -> None:
        """Hold current position with torque."""
        self._write(Action.HOLD)

    def move_deg(self, degrees: float) -> None:
        """Move to absolute position in degrees.

        Args:
            degrees: Target position in degrees
        """
        self._write(Action.MOVE, int(degrees * 10))

    def move_relative_deg(self, degrees: float) -> None:
        """Move relative to current position in degrees.

        Args:
            degrees: Relative position in degrees
        """
        self._write(Action.MOVE_RELATIVE, int(degrees * 10))

    def wheel_deg_per_sec(self, degrees_per_sec: float) -> None:
        """Continuous rotation at specified speed in degrees per second.

        Args:
            degrees_per_sec: Speed in degrees per second
        """
        self._write(Action.WHEEL, int(degrees_per_sec * 10))

    def wheel_rpm(self, rpm: int) -> None:
        """Continuous rotation at specified RPM.

        Args:
            rpm: Speed in RPM
        """
        self._write(Action.WHEEL_RPM, rpm)

    # Query methods

    def get_status(self) -> int:
        """Get servo status."""
        self._write(Query.STATUS)
        return self._read_int(Query.STATUS)

    def get_origin_offset_deg(self, query_type: QueryType = QueryType.SESSION) -> float:
        """Get origin offset in degrees."""
        self._write(Query.ORIGIN_OFFSET, query_type)
        result = self._read_int(Query.ORIGIN_OFFSET)
        return result / 10.0

    def get_angular_range_deg(self, query_type: QueryType = QueryType.SESSION) -> float:
        """Get angular range in degrees."""
        self._write(Query.ANGULAR_RANGE, query_type)
        result = self._read_int(Query.ANGULAR_RANGE)
        return result / 10.0

    def get_position_pulse(self) -> int:
        """Get position in pulse units."""
        self._write(Query.POSITION_PULSE)
        return self._read_int(Query.POSITION_PULSE)

    def get_position_deg(self) -> float:
        """Get position in degrees."""
        self._write(Query.POSITION)
        result = self._read_int(Query.POSITION)
        return result / 10.0

    def get_speed_deg_per_sec(self) -> float:
        """Get current speed in degrees per second."""
        self._write(Query.SPEED)
        result = self._read_int(Query.SPEED)
        return result / 10.0

    def get_speed_rpm(self) -> int:
        """Get current speed in RPM."""
        self._write(Query.SPEED_RPM)
        return self._read_int(Query.SPEED_RPM)

    def get_speed_pulse(self) -> int:
        """Get current speed in pulse units."""
        self._write(Query.SPEED_PULSE)
        return self._read_int(Query.SPEED_PULSE)

    def get_max_speed_deg(self, query_type: QueryType = QueryType.SESSION) -> float:
        """Get maximum speed in degrees per second."""
        self._write(Query.MAX_SPEED, query_type)
        result = self._read_int(Query.MAX_SPEED)
        return result / 10.0

    def get_max_speed_rpm(self, query_type: QueryType = QueryType.SESSION) -> int:
        """Get maximum speed in RPM."""
        self._write(Query.MAX_SPEED_RPM, query_type)
        return self._read_int(Query.MAX_SPEED_RPM)

    def get_color_led(self, query_type: QueryType = QueryType.SESSION) -> int:
        """Get LED color."""
        self._write(Query.COLOR_LED, query_type)
        return self._read_int(Query.COLOR_LED)

    def get_gyre(self, query_type: QueryType = QueryType.SESSION) -> int:
        """Get gyre direction."""
        self._write(Query.GYRE, query_type)
        return self._read_int(Query.GYRE)

    def get_first_position_deg(self) -> float:
        """Get first position in degrees (returns 0 if disabled)."""
        self._write(Query.FIRST_POSITION)
        result = self._read_int(Query.FIRST_POSITION)
        return result / 10.0

    def get_is_first_position_enabled(self) -> bool:
        """Check if first position is enabled."""
        try:
            self._write(Query.FIRST_POSITION)
            self._read_int(Query.FIRST_POSITION)
            return True
        except Exception:
            return False

    def get_model(self) -> str:
        """Get servo model string."""
        self._write(Query.MODEL_STRING)
        return self._read_str(Query.MODEL_STRING, 7)

    def get_serial_number(self) -> int:
        """Get servo serial number."""
        self._write(Query.SERIAL_NUMBER)
        return self._read_int(Query.SERIAL_NUMBER)

    def get_firmware_version(self) -> int:
        """Get firmware version."""
        self._write(Query.FIRMWARE_VERSION)
        return self._read_int(Query.FIRMWARE_VERSION)

    def get_voltage(self) -> int:
        """Get voltage in mV."""
        self._write(Query.VOLTAGE)
        return self._read_int(Query.VOLTAGE)

    def get_temperature(self) -> int:
        """Get temperature in 1/10 degrees Celsius."""
        self._write(Query.TEMPERATURE)
        return self._read_int(Query.TEMPERATURE)

    def get_current(self) -> int:
        """Get current in mA."""
        self._write(Query.CURRENT)
        return self._read_int(Query.CURRENT)

    def get_angular_stiffness(self, query_type: QueryType = QueryType.SESSION) -> int:
        """Get angular stiffness."""
        self._write(Query.ANGULAR_STIFFNESS, query_type)
        return self._read_int(Query.ANGULAR_STIFFNESS)

    def get_angular_holding_stiffness(
        self, query_type: QueryType = QueryType.SESSION
    ) -> int:
        """Get angular holding stiffness."""
        self._write(Query.ANGULAR_HOLDING_STIFFNESS, query_type)
        return self._read_int(Query.ANGULAR_HOLDING_STIFFNESS)

    def get_angular_acceleration(
        self, query_type: QueryType = QueryType.SESSION
    ) -> int:
        """Get angular acceleration."""
        self._write(Query.ANGULAR_ACCELERATION, query_type)
        return self._read_int(Query.ANGULAR_ACCELERATION)

    def get_angular_deceleration(
        self, query_type: QueryType = QueryType.SESSION
    ) -> int:
        """Get angular deceleration."""
        self._write(Query.ANGULAR_DECELERATION, query_type)
        return self._read_int(Query.ANGULAR_DECELERATION)

    def get_is_motion_control_enabled(self) -> int:
        """Check if motion control is enabled."""
        self._write(Query.ENABLE_MOTION_CONTROL)
        return self._read_int(Query.ENABLE_MOTION_CONTROL)

    def get_blinking_led(self) -> int:
        """Get LED blinking configuration."""
        self._write(Query.BLINKING_LED)
        return self._read_int(Query.BLINKING_LED)

    def set_origin_offset_deg(
        self, degrees: float, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set origin offset in degrees.

        Args:
            degrees: Offset position in degrees
            set_type: SESSION or CONFIG
        """
        pos = int(degrees * 10)
        if set_type == SetType.SESSION:
            self._write(Action.ORIGIN_OFFSET, pos)
        else:
            self._write(Config.ORIGIN_OFFSET, pos)

    def set_angular_range_deg(
        self, degrees: float, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set angular range in degrees.

        Args:
            degrees: Range in degrees
            set_type: SESSION or CONFIG
        """
        delta = int(degrees * 10)
        if set_type == SetType.SESSION:
            self._write(Action.ANGULAR_RANGE, delta)
        else:
            self._write(Config.ANGULAR_RANGE, delta)

    def set_max_speed_deg_per_sec(
        self, degrees_per_sec: float, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set maximum speed in degrees per second.

        Args:
            degrees_per_sec: Speed in degrees per second
            set_type: SESSION or CONFIG
        """
        speed = int(degrees_per_sec * 10)
        if set_type == SetType.SESSION:
            self._write(Action.MAX_SPEED, speed)
        else:
            self._write(Config.MAX_SPEED, speed)

    def set_max_speed_rpm(self, rpm: int, set_type: SetType = SetType.SESSION) -> None:
        """Set maximum speed in RPM.

        Args:
            rpm: Speed in RPM
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.MAX_SPEED_RPM, rpm)
        else:
            self._write(Config.MAX_SPEED_RPM, rpm)

    def set_color_led(self, color: int, set_type: SetType = SetType.SESSION) -> None:
        """Set LED color.

        Args:
            color: Color code (use LedColor enum)
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.COLOR_LED, color)
        else:
            self._write(Config.COLOR_LED, color)

    def set_gyre(self, gyre: int, set_type: SetType = SetType.SESSION) -> None:
        """Set gyre direction.

        Args:
            gyre: Direction (use GyreDirection enum)
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.GYRE_DIRECTION, gyre)
        else:
            self._write(Config.GYRE_DIRECTION, gyre)

    def set_first_position_deg(self, degrees: float) -> None:
        """Set first position in degrees.

        Args:
            degrees: Position in degrees
        """
        self._write(Config.FIRST_POSITION, int(degrees * 10))

    def clear_first_position(self) -> None:
        """Clear (disable) first position."""
        self._write(Config.FIRST_POSITION)

    def set_mode(self, mode: int) -> None:
        """Set operating mode.

        Args:
            mode: Mode (use Mode enum)
        """
        self._write(Config.MODE, mode)

    def set_angular_stiffness(
        self, value: int, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set angular stiffness.

        Args:
            value: Stiffness value
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.ANGULAR_STIFFNESS, value)
        else:
            self._write(Config.ANGULAR_STIFFNESS, value)

    def set_angular_holding_stiffness(
        self, value: int, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set angular holding stiffness.

        Args:
            value: Holding stiffness value
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.ANGULAR_HOLDING_STIFFNESS, value)
        else:
            self._write(Config.ANGULAR_HOLDING_STIFFNESS, value)

    def set_angular_acceleration(
        self, value: int, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set angular acceleration.

        Args:
            value: Acceleration value
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.ANGULAR_ACCELERATION, value)
        else:
            self._write(Config.ANGULAR_ACCELERATION, value)

    def set_angular_deceleration(
        self, value: int, set_type: SetType = SetType.SESSION
    ) -> None:
        """Set angular deceleration.

        Args:
            value: Deceleration value
            set_type: SESSION or CONFIG
        """
        if set_type == SetType.SESSION:
            self._write(Action.ANGULAR_DECELERATION, value)
        else:
            self._write(Config.ANGULAR_DECELERATION, value)

    def set_motion_control_enabled(self, value: int) -> None:
        """Enable or disable motion control.

        Args:
            value: 1 to enable, 0 to disable
        """
        self._write(Action.ENABLE_MOTION_CONTROL, value)

    def set_blinking_led(self, state: int) -> None:
        """Set LED blinking configuration.

        Args:
            state: Bitmask of states to blink on
        """
        self._write(Config.BLINKING_LED, state)
