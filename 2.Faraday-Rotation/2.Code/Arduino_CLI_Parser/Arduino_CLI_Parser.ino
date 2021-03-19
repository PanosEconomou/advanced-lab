// Include necessary libraries
#include <Stepper.h>
#include "A4988.h"

#define LED_PIN 13
#define STEP_PIN 6
#define DIR_PIN 5
#define STEPS 800
#define SERVO_PIN 11

A4988 stepper(STEPS,DIR_PIN,STEP_PIN);
double current_angle = 0;
long message = 0;


void setup() {
  // Setup LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Setup Serial Communication
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Initialize Stepper Motor
  stepper.begin(10, 200);
}


////////////////////////////////////////////////////////////////////////////////
// MESSAGE PARSING /////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// Returns 0 if there is no valid command read,
// Returns the integer code of the coomand if there is
long readCommand(){
  int inByte = Serial.read() - '0';
  long cmd = 0;
    
  if (inByte == '\n'-'0') {
    cmd = message;
    message = 0;
  }
  
  else if (inByte >= 0 && inByte <= 9){
    message = message*10 + inByte;
  }

//  Serial.println(String(char(inByte+'0')) + " Message: " + String(message));

  return cmd;
}


// Parses an integer command and executes it
void parse_cmd(long cmd){
  // From the command get the Code and Value
  int AA = int(cmd/10000);
  int XXXX = cmd%10000;

//  Serial.println("Command: "+ String(cmd)+ " AA: " + String(AA)+" XXXX: "+String(XXXX));
  switch(AA){
    case 10:
    set_current_angle(XXXX);
    break;
    
    case 11:
    set_speed(XXXX);
    break;
    
    case 20:
    turn_to(XXXX);
    break;
    
    case 21:
    turn_by(XXXX);
    break;
    
    case 22:
    turn_by(-1*XXXX);
    break; 
    
    case 30:
    send_current_angle();
    break;
  }
}



////////////////////////////////////////////////////////////////////////////////
// SERVO MOVEMENT //////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// Turns by and angle in degrees
void turn_by(double angle){
  stepper.rotate(angle);

  current_angle += angle;
}

// Turns to specific angle
void turn_to(double angle){
  double angle1 = angle-current_angle;
  double angle2 = -(360-angle+current_angle);

  if(abs(angle1) <= abs(angle2)){
    turn_by(angle1);
  }
  else {
    turn_by(angle2);
  }

  current_angle = angle;
}


////////////////////////////////////////////////////////////////////////////////
// OTHER COMMANDS //////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

// Sends the current angle through the serial port
void send_current_angle(){
  Serial.println(current_angle);
}

// Set the current_angle variable
void set_current_angle(int angle){
  current_angle = angle;
}


// Set the speed of the motor
void set_speed(int SPEED){
  stepper.begin(SPEED, 1);
}






void loop() {
  // If there are contents in the Serial Buffer then read them and send them back.
  if (Serial.available()) {
    // Read the command
    long cmd = readCommand();
    
    // If it is a valid command
    if(cmd){
      parse_cmd(cmd);
    }
  }

}
