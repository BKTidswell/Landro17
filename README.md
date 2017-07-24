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
  
* What Needs to Be Done:
  * We need to finalize the number of starting individuals (Currently 5)
  * We need to finalize the fitness function (Currently based on threshold values (Fitness/Offspring 30/1 50/2 90/3))
  * We need to determine the starting range of connection strengths (Currently -4 to 4)
  * We need to finalize the mutation rates (Currently 0.05 mutation and 0.05 duplication)



<コ:彡 
