# Landro17
Code for Landro summer 2017

* Intitial Set Up for Running the Code:
   * Open up terminal on your Mac and type "python", it should show that you have version 2.7 or above
     * If you do not refer to the bottom for a guide to installing python 2.7
   * EvoDevoFull requires a python package that is not included with the default python package
     * This package  is called "numpy", and to get it you will need to get a program called "pip" that lets you download python packages
     * Numpy is used to store genomic information in a form that is easier for EvoDevoFull to read and store between generations
     * First you need to download pip:
        * To do this open up terminal and type "python easy_install pip"
            * If this does not work try "sudo python easy_install pip" and then type your password to complete the installation
     * Next you need to install numpy:
        * To do this open up terminal and type "pip install numpy"
            * If this does not work try "sudo pip install numpy" and then type your password to complete the installation
        * To test that this worked type "python" into a terminal window and then type "import numpy", if there are no errors then the installation worked
  * Now create a folder on your Desktop called "Landro2017" and place EvoDevoFull.py in that folder
    * The folder does not have to be named that exactly, but whatever you call it you must remember, as you will need to type the name to run EvoDevoFull

* What the Code Does:
  * EvoDevoFull does basically what it says, it runs the evolutionary development for the entire population.
  
  * For the first generation it creates a file system labeled "Generation1"
      * This folder has three folders in it labeled "Data", "Genomes", and "Params":
           * The "Params" folder contains all the params.h files for each neural network and are labeled by ID. The params.h files contain a string labled ID so that the datalog produced by that robot will be named by that network's ID
           * The "Genomes" folder contains a numpy array file so that the program can easily read and retrive the genome between generations. It also contains the human readable collection of all genomes, and a collection of ID'd genomes with a verbal output that dictates which nodes connect to what for the network
           * The "Data" folder is the only input that is needed from people. After running Landro with all the params.h files there should be a collection of differently ID'd datalogs that match the params.h files's IDs. Put the datalogs in the "Data" folder to create the next generation.
              * IMPORTANT NOTE: The Data folder is all the input EvoDevoFull needs from you
             
   * Each next generation a similar file system is created labeled "GenerationN" with the same file system inside. EvoDevoFull uses the fitness of each ID'd datalog and matches it to the appropriate genome and mutates it the number of times based on the fitness function to make the new generation.
   
* What You Need to Do with EvoDevoFull:
  * Step 1: Run EvoDevoFull to create the first generation.
    * To run EvoDevoFull type "cd /Desktop/Landro2017" and then after that runs type "python EvoDevoFull.py".
      * If you did not call the folder "Landro2017" please replace that with what you did name the folder
  * Step 2: Run all the params.h files in Landros to get the datalogs.
    * See Section on how to run params.h files for details.
    * Make sure that all the IDs on the datalogs make the params.h IDs!
  * Step 3: Put the datalogs in the "Data" folder of the appropriate generation.
  * Step 4: Run EvoDevoFull to make the next generation.
    * It is run the same way as in Step 1.
   * Repeat until you have run enough generations.
   
* How to Run Params.h Files:
  * Copy all of the params.h files from the appropriate generation and put them in the folder with runLandro2.ino. 
  * Each params.h file represents a different neural netowrk and so they all must be run. 
  * So start with the first one (it will be params####01X#.h) and then put that filename in quotes in line 46.
    * So now it should say #include "params####01X#.h" on that line, so that that neural network will be the one used for the run.
  * Upload the code onto the correct landro, as shown by the X (This will be an A, B, C, or D) in the params.h name, and then put it into the correct arena as shown by the # (1 or 2) after the X.
  * Run Landro until it does its ending song, and then pick it up, unplug the arduino and upload the code again, changing the statement to "#include "params####02X#.h".
  * Repeat this until you have run all the params.h files and then take the data off the SD card and place those files into the "Data" folder of the generation you just ran.
  
* How to Install Python 2.7:
  * This is a short guide on how to install python 2.7. While your Mac should have it, if it does not for any reason then this is the guide for you
  * Go [here](https://www.python.org/downloads/release/python-2713/) and download the Mac OS X 64-bit/32-bit installer.
    * If you do not have Mac OSX 10.6 or above please back up your computer and update it, or find a new computer to do this on
  * After the installer downloads open it and follow the instructions to download and set up python 2.7.13
  * After that is done type python into your terminal window, it should now say the version is 2.7.13
      * If that did not work than you have gone beyond the scope of this guide. Please return having found solutions to your installation issues elsewhere, or return with a Mac with a more up-to-date version of python

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
