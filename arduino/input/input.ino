#include <Streaming.h>

int ledPin = 13;

int pin1a = 22;
int pin1b = 23;
int pin1c = 24;
int pin1d = 25;

int pin2a = 26;
int pin2b = 27;
int pin2c = 28;
int pin2d = 29;

int value = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  pinMode(pin1a, INPUT_PULLUP);
  pinMode(pin1b, INPUT_PULLUP);
  pinMode(pin1c, INPUT_PULLUP);
  pinMode(pin1d, INPUT_PULLUP);
  pinMode(pin2a, INPUT_PULLUP);
  pinMode(pin2b, INPUT_PULLUP);
  pinMode(pin2c, INPUT_PULLUP);
  pinMode(pin2d, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Serial << "Current millis: " << millis() << endl;

  value = ((1 - digitalRead(pin1a)) << 3) + ((1 - digitalRead(pin1b)) << 2) + ((1 - digitalRead(pin1c) << 1)) + (1 - digitalRead(pin1d));

  value += ((1 - digitalRead(pin2a)) << 7) + ((1 - digitalRead(pin2b)) << 6) + ((1 - digitalRead(pin2c) << 5)) + ((1 - digitalRead(pin2d) << 4));

  Serial << value << endl;

  // digitalWrite(ledPin, value);

  delay(100);

  // delay(1000);
}
