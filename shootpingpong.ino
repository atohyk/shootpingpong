#include <Servo.h>

const char shootPin = 3;
const char yawPin = 10;
const char pitchPin = 9;

Servo pitchServo;
Servo yawServo;

unsigned char pitchAngle, yawAngle;
unsigned long lastTime;

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
    delay(500);
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
  lastTime = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    updateSerial(Serial.read());
  }
  if(millis()-lastTime > 1000){
    Serial.print("P");
    Serial.println(pitchAngle);
    Serial.print("Y");
    Serial.println(yawAngle);
    lastTime = millis();
  }
  return;
}
