#include<Servo.h>

Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
  myServo.write(180);
}


String c;
int angle;

void loop() {
  if(Serial.available() > 0){
    c = Serial.readStringUntil('\n');
    angle = c.toInt();
    myServo.write(angle);
  }

}
