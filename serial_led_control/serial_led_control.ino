#include <Arduino.h>

bool ledState = false;
String inputString = "";
bool stringComplete = false;

void printWelcome() {
  Serial.println("Arduino LED Control");
  Serial.println("Commands:");
  Serial.println("  led_on    - Turn LED on");
  Serial.println("  led_off   - Turn LED off");
  Serial.println("  get_led   - Get LED state");
  Serial.println("  [newline] - Show this help");
}

void setup() {
  // put your setup code here, to run once:
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  inputString.reserve(200);  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (stringComplete) {
    if (inputString == "\n") {
      printWelcome();
    }
    else if (inputString == "led_on\n") {
      digitalWrite(LED_BUILTIN, HIGH);
      ledState = true;
      Serial.print("ack led_on\n");
    }
    else if (inputString == "led_off\n") {
      digitalWrite(LED_BUILTIN, LOW);
      ledState = false;
      Serial.print("ack led_off\n");
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
