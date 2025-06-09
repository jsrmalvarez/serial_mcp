import serial
import time
from enum import Enum

class Response(Enum):
    ERROR = "error"
    OK = "ok"
    ON = "on"
    OFF = "off"

class ArduinoSerialControl:
    def __init__(self, port='COM7', baudrate=9600, timeout=1):
        """Initialize serial connection to Arduino.
        
        Args:
            port (str): Serial port
            baudrate (int): Baud rate
            timeout (float): Serial read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None        
        
    def establish_connection(self):
        """Establish serial connection to Arduino."""
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        # Give Arduino time to reset after connection
        time.sleep(2)
        
    def _parse_response(self, response: str) -> tuple[Response, str]:
        """Parse the Arduino response string.
        
        Args:
            response (str): Raw response from Arduino
            
        Returns:
            tuple[Response, str]: (response type, optional message)
        """
        if not response.startswith("ack "):
            return Response.ERROR, response
            
        parts = response.split(" ")
        if len(parts) < 2:
            return Response.ERROR, response
            
        command = parts[1]
        
        if command == "led_on":
            return Response.OK, ""
        elif command == "led_off":
            return Response.OK, ""
        elif command == "get_led":
            if len(parts) < 3:
                return Response.ERROR, response
            return Response.ON if parts[2] == "on" else Response.OFF, ""
            
        return Response.ERROR, response

    def turn_led_on(self) -> Response:
        """Turn the LED on.
        
        Returns:
            Response: OK if successful, ERROR otherwise
        """
        response = self.send_and_receive("led_on")
        status, _ = self._parse_response(response)
        return status

    def turn_led_off(self) -> Response:
        """Turn the LED off.
        
        Returns:
            Response: OK if successful, ERROR otherwise
        """
        response = self.send_and_receive("led_off")
        status, _ = self._parse_response(response)
        return status

    def get_led_status(self) -> Response:
        """Get the current LED status.
        
        Returns:
            Response: ON if LED is on, OFF if LED is off, ERROR if command failed
        """
        response = self.send_and_receive("get_led")
        status, _ = self._parse_response(response)
        return status

    def send_and_receive(self, message, timeout=1.0):
        """Send a message to Arduino and wait for response.
        
        Args:
            message (str): Message to send (newline will be added automatically)
            timeout (float): Maximum time to wait for response in seconds
            
        Returns:
            str: Response from Arduino (without newline)
        """
        # Ensure message ends with newline
        if not message.endswith('\n'):
            message += '\n'
            
        # Send message
        self.serial.write(message.encode())
        
        # Read response until newline or timeout
        response = ''
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.serial.in_waiting:
                char = self.serial.read().decode()
                response += char
                if char == '\n':
                    break
                    
        return response.strip()
    
    def close(self):
        """Close the serial connection."""
        self.serial.close()

def main():
    # Example usage
    arduino = ArduinoSerialControl()
    
    try:
        arduino.establish_connection()
        
        # Test LED control
        print("Turning LED on...")
        response = arduino.turn_led_on()
        print(f"Response: {response}")
        
        time.sleep(1)
        
        print("\nGetting LED status...")
        response = arduino.get_led_status()
        print(f"Response: {response}")
        
        time.sleep(1)
        
        print("\nTurning LED off...")
        response = arduino.turn_led_off()
        print(f"Response: {response}")

        time.sleep(1)
        
        print("\nGetting LED status...")
        response = arduino.get_led_status()
        print(f"Response: {response}")
        
    finally:
        arduino.close()

if __name__ == "__main__":
    main()
