#include <Servo.h>

const char shootPin = 3;
const char yawPin = 10;
const char pitchPin = 9;

Servo pitchServo;
Servo yawServo;

unsigned char pitchAngle, yawAngle;

void updateSerial(char incomingByte) {
  if (incomingByte == 'P') {
    pitchAngle = Serial.parseInt() & 0xFF;
    pitchServo.write(pitchAngle);
    Serial.print("P");
    Serial.println(pitchAngle);
  }
  else if (incomingByte == 'Y') {
    yawAngle = Serial.parseInt() & 0xFF;
    yawServo.write(yawAngle);
    Serial.print("Y");
    Serial.println(yawAngle);
  }
  else if (incomingByte == 'S') {
    Serial.println("Shoot");
    digitalWrite(shootPin, HIGH);
    delay(200);
    digitalWrite(shootPin, LOW);
  }
  return;
}

void setup() {
  // put your setup code here, to run once:
  pitchAngle = 0;
  yawAngle = 0;
  Serial.begin(115200);
  delay(10);
  pinMode(shootPin, OUTPUT);
  pitchServo.attach(pitchPin);
  yawServo.attach(yawPin);
  Serial.println("Start");
  return;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    updateSerial(Serial.read());
  }
  return;
}
