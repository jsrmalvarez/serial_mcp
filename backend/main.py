from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import sys
import os

# Add the parent directory to sys.path to import ArduinoSerialControl
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from python_control.arduino_serial_control import ArduinoSerialControl, Response

app = FastAPI(
    title="Arduino LED Control API",
    description="REST API for controlling Arduino LED via serial communication",
    version="1.0.0"
)

# Pydantic models for responses
class LEDStatus(str, Enum):
    ON = "on"
    OFF = "off"
    ERROR = "error"

class LEDResponse(BaseModel):
    status: str
    message: str = ""

# Global Arduino controller instance
arduino = ArduinoSerialControl()

@app.on_event("startup")
async def startup_event():
    """Initialize Arduino connection when the app starts."""
    try:
        arduino.establish_connection()
    except Exception as e:
        print(f"Error connecting to Arduino: {e}")
        # We don't raise an exception here to allow the app to start
        # Individual endpoints will handle connection issues

@app.on_event("shutdown")
async def shutdown_event():
    """Close Arduino connection when the app shuts down."""
    arduino.close()

@app.get("/led/status", response_model=LEDResponse)
async def get_led_status():
    """Get the current LED status."""
    try:
        status = arduino.get_led_status()
        if status == Response.ON:
            return LEDResponse(status=LEDStatus.ON)
        elif status == Response.OFF:
            return LEDResponse(status=LEDStatus.OFF)
        else:
            raise HTTPException(status_code=500, detail="Failed to get LED status")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/led/on", response_model=LEDResponse)
async def turn_led_on():
    """Turn the LED on."""
    try:
        response = arduino.turn_led_on()
        if response == Response.OK:
            return LEDResponse(status="success", message="LED turned on")
        else:
            raise HTTPException(status_code=500, detail="Failed to turn LED on")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/led/off", response_model=LEDResponse)
async def turn_led_off():
    """Turn the LED off."""
    try:
        response = arduino.turn_led_off()
        if response == Response.OK:
            return LEDResponse(status="success", message="LED turned off")
        else:
            raise HTTPException(status_code=500, detail="Failed to turn LED off")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
