#define LED_PIN 13

void setup() {
  // Setup LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Setup Serial Communication
  Serial.begin(115200);
  Serial.setTimeout(1);
}

long message = 0;

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
    case 11:
    case 20:
    case 21:
    case 22:
    case 30:
  }
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
