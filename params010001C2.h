String ID = "010001C2"; 
#define NUM_INPUT 2 
#define NUM_HIDDEN 1 
#define NUM_OUTPUT 3 
 
float input[NUM_INPUT]; 
float hidden[NUM_HIDDEN]; 
float old_hidden[NUM_HIDDEN]; 
float output[NUM_OUTPUT]; 
float old_output[NUM_OUTPUT]; 
 
const int RMILength = 1; 
const int LMILength = 0; 
int RMI[RMILength] = {2}; 
int LMI[LMILength] = {}; 
 
int sensor_to_input[NUM_INPUT] = {15, 6}; 
float input_to_hidden[NUM_INPUT][NUM_HIDDEN] = {{-4.55}, {0}}; 
float hidden_to_hidden[NUM_HIDDEN][NUM_HIDDEN] = {{0}}; 
float hidden_to_output[NUM_HIDDEN][NUM_OUTPUT] = {{0, 0, 0}}; 
float input_to_output[NUM_INPUT][NUM_OUTPUT] = {{-4.38, 3.25, 0}, {0, 0, -3.42}}; 
float output_to_hidden[NUM_OUTPUT][NUM_HIDDEN] = {{-2.93}, {-1.8}, {0}}; 
 
 
 
