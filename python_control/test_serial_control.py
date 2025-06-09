from arduino_serial_control import ArduinoSerialControl
import time

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
