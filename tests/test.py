# Author: Sebastian Plamauer
# License: LGPL-3.0 (GNU Lesser General Public License version 3)

import pytest
from unittest.mock import Mock
from pylss.lss import LSS
from pylss.constants import (
    Action,
    Query,
    QueryType,
    SetType,
)


class TestLSSCommandGeneration:
    """Test that commands are properly formatted."""

    def test_write_command_without_parameter(self):
        """Test command format without parameter."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss._write(Action.RESET)

        mock_bus.write.assert_called_once_with(b"#5RESET\r")

    def test_write_command_with_integer_parameter(self):
        """Test command format with integer parameter."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(10, mock_bus)

        lss._write(Action.MOVE, 1500)

        mock_bus.write.assert_called_once_with(b"#10D1500\r")

    def test_write_command_with_negative_parameter(self):
        """Test command format with negative parameter."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(2, mock_bus)

        lss._write(Action.MOVE, -450)

        mock_bus.write.assert_called_once_with(b"#2D-450\r")

    def test_write_raises_when_bus_not_open(self):
        """Test that writing raises exception when bus is not open."""
        mock_bus = Mock()
        mock_bus.is_open = False
        lss = LSS(5, mock_bus)

        with pytest.raises(Exception, match="Serial bus is not available or not open"):
            lss._write(Action.RESET)

    def test_write_raises_when_bus_is_none(self):
        """Test that writing raises exception when bus is None."""
        mock_bus = None
        lss = LSS(5, mock_bus)  # type: ignore

        with pytest.raises(Exception, match="Serial bus is not available or not open"):
            lss._write(Action.RESET)


class TestLSSResponseParsing:
    """Test response parsing from servo."""

    def test_read_int_valid_response(self):
        """Test reading valid integer response."""
        mock_bus = Mock()
        mock_bus.is_open = True
        # Simulate response: *5QD1234\r
        mock_bus.read.side_effect = [b"*", b"*"]  # First read finds start marker
        mock_bus.read_until.return_value = b"5QD1234\r"

        lss = LSS(5, mock_bus)
        result = lss._read_int(Query.POSITION)

        assert result == 1234

    def test_read_int_negative_value(self):
        """Test reading negative integer response."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"3QD-900\r"

        lss = LSS(3, mock_bus)
        result = lss._read_int(Query.POSITION)

        assert result == -900

    def test_read_int_wrong_servo_id(self):
        """Test error when response has wrong servo ID."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"7QD1234\r"  # Wrong ID

        lss = LSS(5, mock_bus)

        with pytest.raises(Exception, match="Response from wrong servo ID"):
            lss._read_int(Query.POSITION)

    def test_read_int_wrong_command(self):
        """Test error when response has wrong command identifier."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QV1234\r"  # Wrong command

        lss = LSS(5, mock_bus)

        with pytest.raises(Exception, match="Response command mismatch"):
            lss._read_int(Query.POSITION)

    def test_read_int_malformed_response(self):
        """Test error on malformed response."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"INVALID\r"

        lss = LSS(5, mock_bus)

        with pytest.raises(Exception, match="Malformed response"):
            lss._read_int(Query.POSITION)

    def test_read_int_timeout(self):
        """Test timeout when waiting for response."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"", b""]  # Empty reads simulate timeout

        lss = LSS(5, mock_bus)

        with pytest.raises(Exception, match="Timeout waiting for response"):
            lss._read_int(Query.POSITION)

    def test_read_str_valid_response(self):
        """Test reading valid string response."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QMSLSS-ST1\r"

        lss = LSS(5, mock_bus)
        result = lss._read_str(Query.MODEL_STRING, 7)

        assert result == "LSS-ST1"

    def test_read_raises_when_bus_not_open(self):
        """Test that reading raises exception when bus is not open."""
        mock_bus = Mock()
        mock_bus.is_open = False
        lss = LSS(5, mock_bus)

        with pytest.raises(Exception, match="Serial bus is not available or not open"):
            lss._read_int(Query.POSITION)


class TestLSSActionMethods:
    """Test action methods that send commands."""

    def test_reset(self):
        """Test reset command."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(1, mock_bus)

        lss.reset()

        mock_bus.write.assert_called_once_with(b"#1RESET\r")

    def test_limp(self):
        """Test limp command."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(2, mock_bus)

        lss.limp()

        mock_bus.write.assert_called_once_with(b"#2L\r")

    def test_hold(self):
        """Test hold command."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(3, mock_bus)

        lss.hold()

        mock_bus.write.assert_called_once_with(b"#3H\r")

    def test_move_deg(self):
        """Test move_deg converts degrees to tenths."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.move_deg(45.5)

        mock_bus.write.assert_called_once_with(b"#5D455\r")

    def test_move_deg_negative(self):
        """Test move_deg with negative degrees."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.move_deg(-90.3)

        mock_bus.write.assert_called_once_with(b"#5D-903\r")

    def test_move_relative_deg(self):
        """Test move_relative_deg converts degrees to tenths."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.move_relative_deg(10.5)

        mock_bus.write.assert_called_once_with(b"#5MD105\r")

    def test_wheel_deg_per_sec(self):
        """Test wheel_deg_per_sec converts to tenths."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.wheel_deg_per_sec(30.0)

        mock_bus.write.assert_called_once_with(b"#5WD300\r")

    def test_wheel_rpm(self):
        """Test wheel_rpm."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.wheel_rpm(60)

        mock_bus.write.assert_called_once_with(b"#5WR60\r")


class TestLSSQueryMethods:
    """Test query methods that read responses."""

    def test_get_position_deg(self):
        """Test get_position_deg converts tenths to degrees."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QD455\r"

        lss = LSS(5, mock_bus)
        result = lss.get_position_deg()

        assert result == 45.5
        mock_bus.write.assert_called_once_with(b"#5QD\r")

    def test_get_position_pulse(self):
        """Test get_position_pulse returns raw pulse value."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QP12345\r"

        lss = LSS(5, mock_bus)
        result = lss.get_position_pulse()

        assert result == 12345

    def test_get_status(self):
        """Test get_status."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5Q6\r"

        lss = LSS(5, mock_bus)
        result = lss.get_status()

        assert result == 6  # HOLDING

    def test_get_voltage(self):
        """Test get_voltage."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QV12000\r"

        lss = LSS(5, mock_bus)
        result = lss.get_voltage()

        assert result == 12000  # 12V in mV

    def test_get_temperature(self):
        """Test get_temperature."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QT250\r"

        lss = LSS(5, mock_bus)
        result = lss.get_temperature()

        assert result == 250  # 25.0°C

    def test_get_current(self):
        """Test get_current."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QC500\r"

        lss = LSS(5, mock_bus)
        result = lss.get_current()

        assert result == 500  # 500mA

    def test_get_model(self):
        """Test get_model returns string."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QMSLSS-HT1\r"

        lss = LSS(5, mock_bus)
        result = lss.get_model()

        assert result == "LSS-HT1"

    def test_get_serial_number(self):
        """Test get_serial_number."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QN123456\r"

        lss = LSS(5, mock_bus)
        result = lss.get_serial_number()

        assert result == 123456

    def test_get_firmware_version(self):
        """Test get_firmware_version."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QF368\r"

        lss = LSS(5, mock_bus)
        result = lss.get_firmware_version()

        assert result == 368

    def test_get_speed_deg_per_sec(self):
        """Test get_speed_deg_per_sec converts tenths to degrees."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QWD300\r"

        lss = LSS(5, mock_bus)
        result = lss.get_speed_deg_per_sec()

        assert result == 30.0

    def test_get_speed_rpm(self):
        """Test get_speed_rpm."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QWR60\r"

        lss = LSS(5, mock_bus)
        result = lss.get_speed_rpm()

        assert result == 60

    def test_get_origin_offset_deg_with_query_type(self):
        """Test get_origin_offset_deg with SESSION query type."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QO50\r"

        lss = LSS(5, mock_bus)
        result = lss.get_origin_offset_deg(QueryType.SESSION)

        assert result == 5.0
        mock_bus.write.assert_called_once_with(b"#5QO0\r")

    def test_get_angular_range_deg_config(self):
        """Test get_angular_range_deg with CONFIG query type."""
        mock_bus = Mock()
        mock_bus.is_open = True
        mock_bus.read.side_effect = [b"*"]
        mock_bus.read_until.return_value = b"5QAR1800\r"

        lss = LSS(5, mock_bus)
        result = lss.get_angular_range_deg(QueryType.CONFIG)

        assert result == 180.0
        mock_bus.write.assert_called_once_with(b"#5QAR1\r")


class TestLSSConfigurationMethods:
    """Test configuration setter methods."""

    def test_set_origin_offset_deg_session(self):
        """Test set_origin_offset_deg with SESSION type."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_origin_offset_deg(5.0, SetType.SESSION)

        mock_bus.write.assert_called_once_with(b"#5O50\r")

    def test_set_origin_offset_deg_config(self):
        """Test set_origin_offset_deg with CONFIG type."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_origin_offset_deg(5.0, SetType.CONFIG)

        mock_bus.write.assert_called_once_with(b"#5CO50\r")

    def test_set_max_speed_deg_per_sec_session(self):
        """Test set_max_speed_deg_per_sec with SESSION type."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_max_speed_deg_per_sec(90.0, SetType.SESSION)

        mock_bus.write.assert_called_once_with(b"#5SD900\r")

    def test_set_max_speed_rpm_config(self):
        """Test set_max_speed_rpm with CONFIG type."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_max_speed_rpm(30, SetType.CONFIG)

        mock_bus.write.assert_called_once_with(b"#5CSR30\r")

    def test_set_color_led(self):
        """Test set_color_led."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_color_led(3)  # BLUE

        mock_bus.write.assert_called_once_with(b"#5LED3\r")

    def test_set_gyre(self):
        """Test set_gyre."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_gyre(-1, SetType.SESSION)  # COUNTER_CLOCKWISE

        mock_bus.write.assert_called_once_with(b"#5G-1\r")

    def test_set_first_position_deg(self):
        """Test set_first_position_deg."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_first_position_deg(0.0)

        mock_bus.write.assert_called_once_with(b"#5CFD0\r")

    def test_clear_first_position(self):
        """Test clear_first_position."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.clear_first_position()

        mock_bus.write.assert_called_once_with(b"#5CFD\r")

    def test_set_angular_stiffness(self):
        """Test set_angular_stiffness."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_angular_stiffness(4, SetType.SESSION)

        mock_bus.write.assert_called_once_with(b"#5AS4\r")

    def test_set_motion_control_enabled(self):
        """Test set_motion_control_enabled."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.set_motion_control_enabled(1)

        mock_bus.write.assert_called_once_with(b"#5EM1\r")


class TestLSSEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_servo_id_zero(self):
        """Test with servo ID 0."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(0, mock_bus)

        lss.reset()

        mock_bus.write.assert_called_once_with(b"#0RESET\r")

    def test_servo_id_max(self):
        """Test with maximum servo ID 254."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(254, mock_bus)

        lss.reset()

        mock_bus.write.assert_called_once_with(b"#254RESET\r")

    def test_large_position_value(self):
        """Test with large position values."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.move_deg(1800.0)  # 180 degrees * 10

        mock_bus.write.assert_called_once_with(b"#5D18000\r")

    def test_negative_position_value(self):
        """Test with negative position values."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.move_deg(-1800.0)

        mock_bus.write.assert_called_once_with(b"#5D-18000\r")

    def test_fractional_degrees_rounding(self):
        """Test that fractional degrees are properly converted."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.move_deg(12.34)

        # 12.34 * 10 = 123.4, int() truncates to 123
        mock_bus.write.assert_called_once_with(b"#5D123\r")


class TestLSSObjectLifecycle:
    """Test object initialization and cleanup."""

    def test_init_sets_servo_id(self):
        """Test that __init__ sets servo_id correctly."""
        mock_bus = Mock()
        lss = LSS(42, mock_bus)

        assert lss.servo_id == 42

    def test_init_sets_bus(self):
        """Test that __init__ sets bus correctly."""
        mock_bus = Mock()
        lss = LSS(5, mock_bus)

        assert lss.bus is mock_bus

    def test_init_sets_timeout(self):
        """Test that __init__ sets bus timeout."""
        mock_bus = Mock()
        LSS(5, mock_bus)

        assert mock_bus.timeout == 100  # TIMEOUT_MS

    def test_del_closes_open_bus(self):
        """Test that __del__ closes an open bus."""
        mock_bus = Mock()
        mock_bus.is_open = True
        lss = LSS(5, mock_bus)

        lss.__del__()

        mock_bus.close.assert_called_once()

    def test_del_skips_closed_bus(self):
        """Test that __del__ doesn't close already closed bus."""
        mock_bus = Mock()
        mock_bus.is_open = False
        lss = LSS(5, mock_bus)

        lss.__del__()

        mock_bus.close.assert_not_called()

    def test_del_handles_none_bus(self):
        """Test that __del__ handles None bus gracefully."""
        lss = LSS(5, None)  # type: ignore

        # Should not raise exception
        lss.__del__()
