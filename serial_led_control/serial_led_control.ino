#include <Arduino.h>

bool ledState = false;
String inputString = "";
bool stringComplete = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  inputString.reserve(200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (stringComplete) {
    if (inputString == "led_on\n") {
      digitalWrite(LED_BUILTIN, HIGH);
      ledState = true;
      Serial.print("ack\n");
    }
    else if (inputString == "led_off\n") {
      digitalWrite(LED_BUILTIN, LOW);
      ledState = false;
      Serial.print("ack\n");
    }
    else if (inputString == "get_led\n") {
      Serial.print(ledState ? "on\n" : "off\n");
    }
    
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
