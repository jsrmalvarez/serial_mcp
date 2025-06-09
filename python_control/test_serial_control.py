import pytest
import time
from arduino_serial_control import ArduinoSerialControl, Response

@pytest.fixture
def arduino():
    """Fixture to provide an ArduinoSerialControl instance."""
    controller = ArduinoSerialControl()
    controller.establish_connection()
    yield controller
    controller.close()

def test_led_control(arduino):
    """Test the LED control functionality."""
    # Turn LED on
    response = arduino.turn_led_on()
    assert response == Response.OK

    # Check LED status is ON
    time.sleep(0.1)  # Small delay to ensure Arduino processed command
    response = arduino.get_led_status()
    assert response == Response.ON

    # Turn LED off
    response = arduino.turn_led_off()
    assert response == Response.OK

    # Check LED status is OFF
    time.sleep(0.1)  # Small delay to ensure Arduino processed command
    response = arduino.get_led_status()
    assert response == Response.OFF

def test_led_status_after_on(arduino):
    """Test that LED status correctly reports ON after turning on."""
    response = arduino.turn_led_on()
    assert response == Response.OK
    
    time.sleep(0.1)
    response = arduino.get_led_status()
    assert response == Response.ON

def test_led_status_after_off(arduino):
    """Test that LED status correctly reports OFF after turning off."""
    response = arduino.turn_led_off()
    assert response == Response.OK
    
    time.sleep(0.1)
    response = arduino.get_led_status()
    assert response == Response.OFF
