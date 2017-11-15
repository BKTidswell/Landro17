
/************************************************************/
#include <SoftwareSerial.h>
#include <SPI.h>
#include <SD.h>
#include "params.h"

#define ROBOT 'C'

/*The baud rate change (BRC, or "baud" for short) is
 *a digitial pin that can be used for telling the iRobot
 *Create 2 to change the baud rate at which it communicates.
 *The Create 2's default baud rate is expecting a mini DIN
 *to USB connection with a full sized computer (e.g. PC).
 *Since we are communicating via an Arduino Mega 2560, we
 *want to change this baud rate to be more Arduino friendly.
 *The baud rate of choice shall be 19200, which for simplicity
 *shall also be used to perform actions when interfacing with
 *the micro SD shield.
*/
#define baudPin  11
/*There is a momentary button soldered onto L16A's breakout
 * board.  This button is wired into a digital port.  It can
 * be plugged into any digital port, the one below was
 * convenient at the time of writing this program.
 */
#define contPin  2
/* The chip select pin is a reserved pin on Arduinos
 * (pin 53 for the Mega 2560), which in this context is
 * used to initialize the Catalex SD Card Adapter.
 */
#define chipSelect 53

#define NUM_PORTS 16
/* STANDARDIZE FORMAT....
 *  ports specifies all of the ports available to L16A.
 *  All prots are specified because the fitness function
 *  requires input from all sensors, even if the ANN
 *  only uses a subset.
 */
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
int checkBumpSensors();

/**********************************************************/
/*This moves Landro according to how we want to the bump
 * response to occur. Here we just have it turn 180 and then
 * continue moving.
 */
//void bumpResponse();
void getBumped(int bumpInt);

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

int firstTime = 0;
bool firstRec = true;

float preRMSPD = random(0,500);
float preLMSPD = random(0,500);

//https://cdn-shop.adafruit.com/datasheets/create_2_Open_Interface_Spec.pdf
/**********************************************************/
void setup() {

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
  Serial.begin(115200);
//  while (!Serial) {
//    ; // wait for serial port to connect. Needed for native USB port only
//  }


  Serial.print("Initializing SD card...");

  //See if the SD card is present and can be initialized:
  while (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    //return;
  }
  Serial.println("card initialized.");


  //NBL: Might not use this during evolutionary experiments.
  //But may be a way to transition from trial to trial or something.
  //Whether for a single individual, or between individuals.

  pinMode(contPin, INPUT);

  //Initialize sensor values
  for (int i = 0; i < numPorts; i++) {
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

void loop() {
  delay(500);
  int Speed = 200;
  float rMod;
  float lMod;

  if(ROBOT == 'A'){
    rMod = 0.93;
    lMod = 1;
  }
  else if(ROBOT == 'B'){
    rMod = 1;
    lMod = 0.96;
  }
  else if(ROBOT == 'C'){
    rMod = 0.97;
    lMod = 1;
  }
  else if(ROBOT == 'D'){
    rMod = 1;
    lMod = 0.95;
  }

  Serial.println("Driving now");
  
  driveMotors(Speed * rMod, Speed * lMod);

}


/**********************************************************/
/*Sends two bytes per motor.  The bytes cannot be written
 * as one continuous string, so they are broken up and
 * sent in serial.  Before sending the values, however, make
 * sure they fall between -500 and 500 by calling checkSpeed().
 */
void driveMotors(int rightValue, int leftValue) {
  Serial3.write(145);//Creat 2's motor command code.
  Serial3.write(highByte(rightValue));//High and low byte for the right motor.
  Serial3.write(lowByte(rightValue));
  Serial3.write(highByte(leftValue));//High and low byte for the left motor.
  Serial3.write(lowByte(leftValue));
}





