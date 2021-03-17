#include <Stepper.h>
#include "A4988.h"

#define STEP_PIN 6
#define DIR_PIN 5
#define STEPS 800
#define LED_PIN 13
#define SERVO_PIN 11

A4988 stepper(STEPS,DIR_PIN,STEP_PIN);
double current_angle = 0;
bool SW;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
 
  pinMode(LED_PIN,OUTPUT);
  digitalWrite(LED_PIN,LOW);

  stepper.begin(10, 1);
  SW = false;
}

// Turns by and angle in degrees
void turn_by(double angle){
  stepper.rotate(angle);

  current_angle += angle;
}


// Turns to specific angle
void turn_to(double angle){
  double angle1 = angle-current_angle;
  double angle2 = -(360-angle+current_angle);

  if(abs(angle1) >= abs(angle2)){
    turn_by(angle1);
  }
  else {
    turn_by(angle2);
  }

  current_angle = angle;
}

void loop() {
//  stepper.step(500);
  if(Serial.available()){
    int x = Serial.readString().toInt();
    if (x<0) digitalWrite(LED_PIN,LOW);
    if (x>=0)digitalWrite(LED_PIN,HIGH);
    turn_by(x);
  }
}
