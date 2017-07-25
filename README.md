# Landro17
Code for Landro summer 2017

* Set Up for Running the Code:
   * Random, os, and math should already be there
   * To run EvoDevo full you should only need to download numpy, and I would advise using pip to do that. 
   * I used python version 2.7 to develop this

* What the Code Does:
  * EvoDevoFull does basically what it says, it runs the evolutionary development for the entire population.
  
  * For the first generation it creates a file system labeled "Generation1"
      * This folder has three folders in it labeled "Data", "Genomes", and "Params":
           * The "Params" folder contains all the params.h files for each neural network and are labeled by ID. The params.h files contain a string labled ID so that the datalog produced by that robot will be named by that network's ID
           * The "Genomes" folder contains a numpy array file so that the program can easily read and retrive the genome between generations. It also contains the human readable collection of all genomes, and a collection of ID'd genomes with a verbal output that dictates which nodes connect to what for the network
           * The "Data" folder is the only input that is needed from people. After running Landro with all the params.h files there should be a collection of differently ID'd datalogs that match the params.h files's IDs. Put the datalogs in the "Data" folder to create the next generation.
             
   * Each next generation a similar file system is created labeled "GenerationN" with the same file system inside. EvoDevoFull uses the fitness of each ID'd datalog and matches it to the appropriate genome and mutates it the number of times based on the fitness function to make the new generation.
   
* What You Need to Do with EvoDevoFull:
  * Step 1: Run EvoDevoFull to create the first generation
  * Step 2: Run all the params.h files in Landros to get the datalogs
    * Make sure that all the IDs on the datalogs make the params.h IDs!
  * Step 3: Put the datalogs in the "Data" folder of the appropriate generation
  * Step 4: Run EvoDevoFull to make the next generation
   * Repeat until you have run enough generations
   
* How to Run Params.h Files:
  * Copy all of the params.h files from the appropriate generation and put them in the folder with runLandro2.ino. 
  * Each params.h file represents a different neural netowrk and so they all must be run. 
  * So start with the first one (it will be params####01X#.h) and then put that file name in quotes in line 46
  * So now it should say #include "params####01X#.h" on that line, so that neural netowrk will be the one used for the run
  * Upload the code onto the correct landro, as shown by the X in the params.h name, and then put it into the correct arena as shown by the # after the X
  * Run Landro until it does its ending song, and then pick it up, unplug the arduino and upload the code again, changing the statement to #include "params####02X#.h"
  * Repeat this until you have run all the params.h files and then take the data off the SD card and place those files into the "Data" folder of the generation you just ran
  
* What Needs to Be Done:
  * We need to finalize the number of starting individuals (Currently 5)
  * We need to finalize the reporduction rules (Currently based on threshold values (Fitness/Offspring 30/1 50/2 90/3))
  * We need to determine the starting range of connection strengths (Currently -4 to 4)
  * We need to finalize the mutation rates (Currently 0.05 mutation and 0.05 duplication)
  * We need to determine what velocities, growth rates, and and times we want for development (5,3, and 100 currently)
  * We need to finalize fitness function (Currently no wiring cost or build cost, just the additive and multiplicative XOR fitness)

* What We Have Decided:
  * For number of genes we will have a mean of 10 and a standard deviation of 2 so that the mean is 50% viable




<コ:彡 
