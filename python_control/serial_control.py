import serial
import time

class ArduinoSerialControl:
    def __init__(self, port='COM8', baudrate=9600, timeout=1):
        """Initialize serial connection to Arduino.
        
        Args:
            port (str): Serial port (default: 'COM8')
            baudrate (int): Baud rate (default: 9600)
            timeout (float): Serial read timeout in seconds (default: 1)
        """
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        # Give Arduino time to reset after connection
        time.sleep(2)
        
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
        # Test LED control
        print("Turning LED on...")
        response = arduino.send_and_receive("led_on")
        print(f"Response: {response}")
        
        time.sleep(1)
        
        print("\nGetting LED status...")
        response = arduino.send_and_receive("get_led")
        print(f"Response: {response}")
        
        time.sleep(1)
        
        print("\nTurning LED off...")
        response = arduino.send_and_receive("led_off")
        print(f"Response: {response}")

        time.sleep(1)
        
        print("\nGetting LED status...")
        response = arduino.send_and_receive("get_led")
        print(f"Response: {response}")
        
    finally:
        arduino.close()

if __name__ == "__main__":
    main()
