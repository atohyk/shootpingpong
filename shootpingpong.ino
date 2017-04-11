#include <Servo.h>
#define RX_BUFFER_SIZE 10
#define MSG_SHOOT_ID 1
#define MSG_AIM_ID 2

const char shootPin = 9;
const char yawPin = 10;
const char pitchPin = 3;

Servo pitchServo;
Servo yawServo;

char rxBuffer[RX_BUFFER_SIZE];

typedef struct {
  char msgID,
  unsigned char msgLength;
  unsigned char pitchAngle, yawAngle;
}SerialMsg_t;

SerialMsg_t serialMsg;

enum {
  WAITING_FOR_MSG_ID,
  WAITING_FOR_PITCH,
  WAITING_FOR_YAW,
} serialState;

void shootPingPong(){
  //set D pin to high 
  digitalWrite(shootPin, HIGH);
  delay(200);
  digitalWrite(shootPin, LOW);
}
void updateSerial(char incomingByte){
  switch (serialState){
    case WAITING_FOR_MSG_ID:
     if(incomingByte == 'P'){
      serialState = WAITING_FOR_PITCH;
     }
     else if(incomingByte == 'Y'){
      serialState = WAITING_FOR_YAW;
     }
     else if(incomingByte == 'S'){
      shootPingPong();
     }
     else{
      //reset
      memset(&serialMsg, 0, sizeof(serialMsg));
     }
     break;
    case WAITING_FOR_PITCH:
      serialMsg.pitchAngle = Serial.parseInt();
      pitchServo.write(serialMsg.pitchAngle);
      serialState = WAITING_FOR_MSG_ID;
      break;
    case WAITING_FOR_YAW:
      serialMsg.yawAngle = Serial.parseInt();
      yawServo.write(serialMsg.yawAngle);
      serialState = WAITING_FOR_MSG_ID;
      break;
     }
}

void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 delay(10);
 pinMode(shootPin, OUTPUT);
 pitchServo.attach(pitchPin);
 yawServo.attach(yawPin);
 memset(&rxBuffer[0], 0, sizeof(rxBuffer));
 memset(&serialMsg, 0, sizeof(serialMsg));
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    updateSerial(Serial.read());
  }
}
