
#include <SoftwareSerial.h>
#include <SPI.h>
#include <SD.h> 
#include "params.h"


#define baudPin  11

#define contPin  2

#define chipSelect 53

#define NUM_PORTS 16

int ports[NUM_PORTS];
/**********************************************************/
/* This function runs through every available sensor, and
 * obtains the value for that sensor for the current timestep. 
 * That value gets stored in the appropriate input node of the
 * ANN.  In essence, sense() tells the ANN about the world on a
 * given iteration.
 */
void sense();
/**********************************************************/
/* This function executes the computations of L16A's ANN.
 */
 void neural_net();
 /**************************************************************/
/* This function implements the activation function for updating
 * network nodes(specifically hidden nodes).  There are two
 * slightly different formulations, one for recurrent connections
 * and one for non-recurrent connections.
 */
float activation(float value);
/**********************************************************/
/*This function records all experimentally relevant data to
 *a micro SD card.  These are the data that will be used
 *to analyze the experiment, and to compute an individual's
 *fitness.
 */
void record();
/**********************************************************/
/*This function takes two values which should range between
 * -500 and 500 (ostensibly with units of mm/sec) and sends
 * those values to the Create 2 as a sequence of four bytes
 * (two per motor), which instruct the Create 2 motors how
 * to drive.  Negative values for rightValue and leftValue
 * cause the motors to spin backward.  Larger values denote
 * faster spin.
 */
void driveMotors(int rightValue, int leftValue);
/**********************************************************/
/*This currently does not work reliably, but it spurpose is to
 * poll the front bumpers of the Create 2.  Which is to say,
 * factory made sensors, not ones installed after the fact.
 * It is somewhat unclear as to what the correct command
 * codes for reading the bumpers are, and what the proper way is
 * to specify what data subset should be read, or how it should
 * be read.
 */
bool checkBumpSensors();

/**********************************************************/
/*This moves Landro according to how we want to the bump 
 * response to occur. Here we just have it turn 180 and then 
 * continue moving.
 */
void bumpResponse();

/**********************************************************/
//Limits speed to a range between -500 and 500 by clipping it.
int checkSpeed(int &spd);


//Declare place for sensor values to be stored
const int numPorts = 16;
const int numSensorSamples = 10;
float sensorValues[numPorts];
float sensorSD[numPorts];
//Specify ports for L16A:
int analogPorts[NUM_PORTS] = {A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13, A14, A15};
int bumpPin0 = 12;
int bumpPin1 = 13;
int bumpRight;
int bumpLeft;
String softStr; 

//for sensor scaling
int minIR = 0;
int maxIR = 750;
int minPhoto = 0;
int maxPhoto = 425; 
  
//https://cdn-shop.adafruit.com/datasheets/create_2_Open_Interface_Spec.pdf
/**********************************************************/
void setup(){
  
  //Give the iRobot Create 2 a chance to "wake up".
  delay(2000);
  //Open communication with iCreate
  pinMode(baudPin, OUTPUT);
  //Set data rate for the SoftwareSerial port, this is the iRobot's default
  Serial3.begin(19200);
  //Send three low signal pulses to the BRC pin to enact the baud rate
  //change that is specified above.
  digitalWrite(baudPin, LOW);
  delay(500);
  digitalWrite(baudPin, LOW);
  delay(500);
  digitalWrite(baudPin, LOW);
  delay(500);
  
  //Start robot in safe mode
  Serial3.write(128);//128 is the "start" code.
  Serial3.write(131);//Safe = 131, Full = 132
  delay(1000);
  // Open serial communications and wait for port to open:
  Serial.begin(19200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  Serial.print("Initializing SD card...");
    
  //See if the SD card is present and can be initialized:
  while (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    //return;
  }
  Serial.println("card initialized.");

  Serial3.write(139);
  Serial3.write(255);
  Serial3.write(1);
  Serial3.write(255);

  Serial3.write(148);
  Serial3.write(1);
  Serial3.write(20);
  
  //NBL: Might not use this during evolutionary experiments.
  //But may be a way to transition from trial to trial or something.
  //Whether for a single individual, or between individuals.

  pinMode(contPin, INPUT);
  
  //Initialize sensor values
  for(int i = 0; i < numPorts; i++){
      sensorValues[i] = 0;
  }


//  Serial3.write(148);
//  Serial3.write(1);
//  Serial3.write(7);
  
  //Do bumper pins
  pinMode(bumpPin0, INPUT);
  pinMode(bumpPin1, INPUT);
}

/***************************************************************/
//This is the main loop of arduino code and calls everything else
// if there are issues something may be commented out here

void loop(){
    
    long loopTime = millis();
    //some bump controls happen here
   if(checkBumpSensors() == true){
      Serial.println("Ow!");
      //bumpResponse();
    }
    
    int i;
    
    //sense();
    //record();
    //neural_net();

   //driveMotors(50,50);
    
    float rmSpeed = 0;
    float lmSpeed = 0;

    for(i = 0; i < RMILength; i++){
      rmSpeed += output[RMI[i]];
    }

    for(i = 0; i < LMILength; i++){
      lmSpeed += output[LMI[i]];
    }

    Serial.println("Left Motor: " + String(motorScale(lmSpeed)) + 
                   " || Right Motor: " + String(motorScale(rmSpeed)));
     
    driveMotors(motorScale(rmSpeed), motorScale(lmSpeed));
    
    Serial.println(String(millis() - loopTime));
}

/***************************************************************/
/* This function uses local variables to loop through L16A's sensors,
 * and store their current values in the "sensorValues" array.  The
 * matrix "analogPorts" names, in sequence, all 16 analog sensor ports
 * (alternating IR and LDR in a clockwise fashion, starting with the
 * former).  The port numbers correspond to the sensor positions, starting with
 * IR1 (which in broader terms is sensor 0), positioned at the exact front of
 * Landro in line with the Create 2 IR beacon sensor.  Moving clockwise, sensor 1
 * is LDR1, which sits immediately to the right of IR1 and plugs into port A1.
 * The pattern continues, and terminates with LDR8 -- sensor 15 -- in port A15.
 * 
 * Each sensor is read 10 times in succession.  The average of these readings
 * will be taken to be "the" sensor value for the current iteration of
 * behavior.  This averaging is done elsewhere.  Though, sensorValues could
 * simply become a one dimensional array, each cell of which is first populated
 * by summing, and then outside of the "j" loop, averaged.
 */
void sense(){
  int i, j;
  
  for(i = 0; i < numPorts; i++){
    for(j = 0; j < numSensorSamples; j++){
      if(i % 2 == 0){
        sensorSD[i] += analogRead(analogPorts[i]);
        sensorValues[i] += irScale(analogRead(analogPorts[i]));
      }
      else{
        sensorSD[i] += analogRead(analogPorts[i]);
        sensorValues[i] += photoScale(analogRead(analogPorts[i]));
      }
    }
    sensorValues[i] = sensorValues[i]/numSensorSamples;
    sensorSD[i] = sensorSD[i]/numSensorSamples;
  }

}
/***************************************************************/
/* This function executes L16A's ANN computations.  This handles
 *  all updates downstream of the inputs array.
 */
void neural_net(){
  int h, p, o, i;

  //update input nodes from sensor values
  for(i = 0; i < NUM_INPUT; i++){
    input[i] = sensorValues[sensor_to_input[i]];
    Serial.println("Input: " + String(input[i]));
  }

  //Update hidden nodes using inputs for time t
  for(h = 0; h < NUM_HIDDEN; h++){
    hidden[h] = 0;
    for(i = 0; i < NUM_INPUT; i++) {   
      hidden[h] = hidden[h] + input[i] * input_to_hidden[i][h];
      if(input_to_hidden[i][h] != 0){
        Serial.print("Input to Hidden: " + String(input[i]));
        Serial.println("  Connect: " + String(input_to_hidden[i][h]));
      }
    }
    //Update hidden nodes using hidden (last) values) from time t-1
    for(p = 0; p < NUM_HIDDEN; p++){
      hidden[h] = hidden[h] + old_hidden[p] * hidden_to_hidden[p][h];
      if(hidden_to_hidden[p][h] != 0){
        Serial.print("Old Hidden to Hidden: " + String(old_hidden[p]));
        Serial.println("  Connect: " + String(hidden_to_hidden[p][h]));
      }
    }
  }
  
  for(h = 0; h < NUM_HIDDEN; h++){
    Serial.print("Hidden: " + String(hidden[h]));
    //Apply tanh function to total update
    hidden[h] = activation(hidden[h]);
    
    //Save the hidden nodes state for the future use
    old_hidden[h] = hidden[h];
    Serial.println(" Tanh Hidden: " + String(hidden[h]));
  }

   //Update output (motor) nodes based on input nodes 
  for(o = 0; o < NUM_OUTPUT; o++){
    output[o] = 0;
    for(i = 0; i < NUM_INPUT; i++){
      output[o] = output[o] + input[i] * input_to_output[i][o];
      if(input_to_output[i][o] != 0){
        Serial.print("Input to Output: " + String(input[i]));
        Serial.println("Connect: " + String(input_to_output[i][o]));
      }
    }
  }
  
  //Update output (motor) nodes based on hidden nodes 
  for(o = 0; o < NUM_OUTPUT; o++){
    for(h = 0; h < NUM_HIDDEN; h++){
      output[o] = output[o] + hidden[h] * hidden_to_output[h][o];
      if(hidden_to_output[h][o] != 0){
        Serial.print("Hidden to Output: " + String(hidden[h]));
        Serial.println("  Connect: " + String(hidden_to_output[h][o]));
      }
    }
    Serial.println("Output: " + String(output[o]));
  }

  for(o = 0; o < NUM_OUTPUT; o++){
    //Apply tanh equation to total update
    output[o] = activation(output[o]);
    Serial.println("Output Tanh: " + String(output[o]));
  }
    
}
/**************************************************************/
/* This function implements the activation function for updating
 * network nodes(specifically hidden nodes).  There are two
 * slightly different formulations, one for recurrent connections
 * and one for non-recurrent connections.
 */
float activation(float value){
  float update_value;
  update_value = tanh(value - 1) + 1;
  return update_value;
}
  
/***************************************************************/
/* This function writes trial information to a micro SD card.
 *  At this point, it is unclear what should be written.
 *  At the bare minimum, it should be ANN inputs and outputs.
 *  There should probably be some sort of time stamp.  Potentially,
 *  all sensors, whether used in the current agent's morphology
 *  or not, should be recorded for use in calculating fitness.
 *  Alternatively, fitness could be calculated on the fly, and
 *  piecewise fitness recorded.  That could be interesting.
 *  Then a running talley could be kept, but performance over time
 *  could also be plotted and analyzed.
 */
void record(){
 //String to store data values
   String data = "";

  File datafile = SD.open("datalog.txt", FILE_WRITE);

  for(int i = 0; i < numPorts; i++){
    data += String(sensorSD[i]) + ",";
  }

  data += "\n";

  for(int i = 0; i < numPorts; i++){
    data += String(sensorValues[i]) + ",";
  }
  
  data += String(millis()) + ",";
  
  //If able, write to SD card
  if(datafile){
    //Write data to serial and SD card
    Serial.println(data);
    datafile.println(data);
    Serial.println("datalog opened succesfully");
  }
  // if the file isn't open, pop up an error:
  else{
    Serial.println(data);
    Serial.println("error opening datalog.txt");
  }

  datafile.close();
}
/**********************************************************/
/*Sends two bytes per motor.  The bytes cannot be written
 * as one continuous string, so they are broken up and
 * sent in serial.  Before sending the values, however, make
 * sure they fall between -500 and 500 by calling checkSpeed().
 */
void driveMotors(int rightValue, int leftValue){
  checkSpeed(rightValue);
  checkSpeed(leftValue);
  Serial3.write(145);//Creat 2's motor command code.
  Serial3.write(highByte(rightValue));//High and low byte for the right motor.
  Serial3.write(lowByte(rightValue));
  Serial3.write(highByte(leftValue));//High and low byte for the left motor.
  Serial3.write(lowByte(leftValue));
}

//This is somewhat complicated and I don't know exactly how it all works
//but it does so that's pretty good. It just reads the byte stream basically
//after asking for the info
//Originally sourced from http://web.ics.purdue.edu/~fwinkler/AD61600_S14/AD61600_Arduino_iRobot.pdf

/*Bumps and Wheel Drops Packet ID: 7 Data Bytes: 1, unsigned
The state of the bumper (0 = no bump, 1 = bump) and wheel drop sensors (0 = wheel raised, 1 = wheel
dropped) are sent as individual bits. */
bool checkBumpSensors() {
      char sensorbytes[10]; // variable to hold the returned 10 bytes
      Serial3.write((byte)142); // get sensor packets
      Serial3.write((byte)7);
      delay(200);

      int i = 0;
      
      while (i < 10) {
      sensorbytes[i++] = 0; 
      }
      
      i = 0;
      
      while(Serial3.available()) { 
        Serial.println("avalible");
        byte c = Serial3.read(); 
        sensorbytes[i++] = c;
        Serial.println(c);
        if(c != 0){
          Serial.println("AHHHHHHHHHHHHHH");
        }
      }
      
      bumpRight = sensorbytes[0] & 0x01;
      bumpLeft = sensorbytes[0] & 0x02;

      if(bumpRight == 1 && bumpLeft == 2){
        return true;
      }
      else{
        return false;
      }
  }

/**************************************************************/
/* If checkBumpSensors was true then this runs and ideally turns
 *  the Landro in a circle so that it is no longer stuck
 */

void bumpResponse(){
  driveMotors(25, 25);
  delay(300);
  driveMotors(0,0);
}

 
/**************************************************************/
/* This funciton pimits speed to a range between -500 and 500 
 * by clipping it.  Speed (spd) is passed by reference, so there 
 * is no need to have an explicit return value.
 */
int checkSpeed(int &spd){
 if(spd > 500){
  spd = 500;
 }
 else if(spd < -500){
  spd = -500;
 }
}

 /********************************************************/
  //Just stops the robot and plays and happy tune to let you
  // know the test is over. Ideally, If you press the button then you 
  // get out of the end test, but that needs to be worked some with Nick
 void endTest(){
    while(true){
          driveMotors(0,0);
          Serial3.write(140);
          //Number 0
          Serial3.write((byte)1);
          //4 Notes
          Serial3.write((byte)4);
          playA();
          playE();
          playB();
          playC();
          //play the song
          Serial3.write(141);
          Serial3.write((byte)1);
        }
  }
  
  void playA(){
    Serial3.write((byte)69);
    Serial3.write((byte)32);
  }
  void playB(){
    Serial3.write((byte)71);
    Serial3.write((byte)32);
  }
  void playC(){
    Serial3.write((byte)72);
    Serial3.write((byte)32);
  }
  void playD(){
    Serial3.write((byte)74);
    Serial3.write((byte)32);
  }
  void playE(){
    Serial3.write((byte)76);
    Serial3.write((byte)32);
  }

 /********************************************************/
  // Maps the tanh values from -1 to 1 to -500 to 500

  float motorScale(float val){
    float fromLow = 0;
    float fromHigh = 2;
    float toLow = 0;
    float toHigh = 500;
    float mapVal = (((val - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow)) + toLow;
    return(mapVal);
  }

 /********************************************************/
  // Maps the irValue values from minIR to maxIR to 0 to 2

  float irScale(int val){
    float fromLow = minIR;
    float fromHigh = maxIR;
    float toLow = 0;
    float toHigh = 2;
    float mapVal = (((val - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow)) + toLow;
    return(mapVal);
  }


 /********************************************************/
  // Maps the photoValue values from minPhoto to maxPhoto to 0 to 2

  float photoScale(int val){
    float fromLow = minPhoto;
    float fromHigh = maxPhoto;
    float toLow = 0;
    float toHigh = 2;
    float mapVal = (((val - fromLow) * (toHigh - toLow)) / (fromHigh - fromLow)) + toLow;
    return(mapVal);
  }
  

