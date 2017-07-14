#define NUM_INPUT 3 
#define NUM_HIDDEN 0 
#define NUM_OUTPUT 2 

String ROBOT = "C";
String ARENA = "1";
 
float input[NUM_INPUT]; 
float hidden[NUM_HIDDEN]; 
float old_hidden[NUM_HIDDEN]; 
float output[NUM_OUTPUT]; 
float old_output[NUM_OUTPUT];
 
const int RMILength = 1; 
const int LMILength = 1; 
int RMI[RMILength] = {0}; 
int LMI[LMILength] = {1}; 
 
int sensor_to_input[NUM_INPUT] = {2,14,8}; 
float input_to_hidden[NUM_INPUT][NUM_HIDDEN] = {{},{},{}}; 
float hidden_to_hidden[NUM_HIDDEN][NUM_HIDDEN] = {}; 
float hidden_to_output[NUM_HIDDEN][NUM_OUTPUT] = {}; 
float input_to_output[NUM_INPUT][NUM_OUTPUT] = {{4,-2},{-2,4},{4,4}}; 
float output_to_hidden[NUM_OUTPUT][NUM_HIDDEN] = {{},{}}; 
 
 
 
