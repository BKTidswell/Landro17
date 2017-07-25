import os
import numpy as np
import random
import math

#The README on github expalins most of the functionality of the code from the user side, so this commenting
# will be primarily for editting of the code itself. Big picture it makes folders that have all the evolutionary
# material for privious generations and the one being currently run. For more big picture and knowing how to 
# run and use this I would say check github

#Important Varibles to change:
# Robot Amount: In makeGenOne(), this is the number of robot in the starting pop

def makeGen():
	#So this bit of code makes the file folder system where everything else is put.
	# It determines what the most recent generation built was and makes the next one 
	# after that. And then makes the three folders in it
	dirDone = False
	count = 1

	while not dirDone:
		dirName = "Generation"+str(count)
		if not os.path.exists(dirName):
			os.makedirs(dirName)
			os.makedirs(dirName+"/Params")
			os.makedirs(dirName+"/Genomes")
			os.makedirs(dirName+"/Data")
			dirDone = True
		else:
			count = count + 1

	#If it's just the first generation it just makes the generation
	# Otherwise it uses the last generation's data to make the current one
	if count == 1:
		makeGenOne()
	else:
		makeNextGen(count)

def makeGenOne():
	allGenomes = []
	allIDs = []

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]

	mean = 10
	sd = 2

	roboAmount = 5

	#This makes all IDs for the first generation
	for x in range(0,0 + roboAmount):
		robotVal = robotArray[random.randint(0,3)]
		arenaVal = arenaArray[random.randint(0,1)]
		#Makes a genome with number of genes on a normal curve
		numGenes = int(np.random.normal(mean,sd,1))
		genome = makeGenome(numGenes)
		allGenomes.append(genome)
		allIDs.append("0100"+str(x).zfill(2)+ robotVal + arenaVal)

	#This writes a human readable genome and an numpy readable genome into the genomes folder
	genomeFile = open("Generation1/Genomes/genomes.txt","w")
	genomeFile.write(str(allGenomes))
	allGenomes = np.asarray(allGenomes)
	np.save("Generation1/Genomes/genomes",allGenomes)
	#print allIDs

	gen = 1

	#runs the devlopment and connections for each robot in the generation
	for i in range(0,len(allIDs)):
		runDevo(allGenomes[i],allIDs[i],gen)


def makeGenome(nGenes):
	maxSpawn = 100
	vMax = 5
	vDurationMin = 0
	vDurationMax = 100
	gMax = 3
	gDurationMin = 0
	gDurationMax = 100
	# 0 = Part Type (0 = IR, 1 = Photo, 2 = Neuron, 3 = R Motor, 4 = L Motor)
	# 1 = Angle
	# 2 = Start Time
	# 3 = Velocity
	# 4 = Travel Time
	# 5 = Growth Rate
	# 6 = Growth Time
	# 7 = Index

	genome = [[0 for x in range(8)] for y in range(nGenes)] 


	#creates a genome
	for i in range(0,nGenes):
		genome[i][0] = random.randint(0,4)
		genome[i][1] = random.randint(0,360)
		genome[i][2] = random.randint(0,maxSpawn)
		genome[i][3] = random.randint(1,vMax)
		genome[i][4] = random.randint(vDurationMin,vDurationMax)
		genome[i][5] = random.randint(1,gMax)
		genome[i][6] = random.randint(gDurationMin,gDurationMax)
		genome[i][7] = i

	return genome

def runDevo(genome,ID,gen):

	count = 0
	connects = []

	#no longer makes an image but just runs trhough the step processes
	#1000 was picked with the idea that it would take a while for the devlopment
	#time to take that long.
	while count < 1000:
		#ProcessCons is run on the connections found on each cycle and updates
		#the connection list so that there are no duplicates
		connects = processCons(devoGraphics(genome, count), connects)
		count = count + 1

	#Returns 0 if it's not viable and 1 if it is (or probably is)
	return makeConnectome(connects,ID,gen,genome)

def devoGraphics(genome, count):

	center = [375,325]

	irPointList = []
	photoPointList = []

	genePosList = []

	currentList = []

	#Moves it using X and Y from the center
	for gene in genome:
		#If we have gone past the start time of the gene then it appears
		if gene[2] <= count:
			#Runs based on the count
			if gene[4]+gene[2] >= count:
				x = int(center[0] + gene[3]*(count-gene[2])*math.cos(math.radians(gene[1])))
				y = int(center[1] + gene[3]*(count-gene[2])*math.sin(math.radians(gene[1])))
			#If it has run for it's full development time then it stops moving
			else:
				x = int(center[0] + gene[3]*gene[4]*math.cos(math.radians(gene[1])))
				y = int(center[1] + gene[3]*gene[4]*math.sin(math.radians(gene[1])))

			#Grows based on count
			if gene[6]+gene[2] >= count:
				size = int(1+gene[5]*(count-gene[2]))
			#Again if it is past the growth time then it stops growing
			else:
				size = int(1+gene[5]*gene[6])

			currentList.append([x,y,size,gene[7]])
	
	#Checks the connections based on where all the seeds are currently
	#Returns a list of then connections made up to this point
	return checkConds(currentList)

def distance(x1,x2,y1,y2):
	#calcualtes distance
	#8**2 is the same as 8^2 or 64
	return (math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def checkConds(currentLocs):
	conList = [] 
	for i in range(0,len(currentLocs)-1):
		for j in range(i+1,len(currentLocs)):
			#For each node it sees if it is within range of any other node by seeing if the 
			# distance is less 
			dist = distance(currentLocs[i][0],currentLocs[j][0],currentLocs[i][1],currentLocs[j][1])
			combRad = currentLocs[i][2] + currentLocs[j][2]
			#if the distance is smaller than the combined radius then these two seeds are put onto
			# the list of connections
			if dist <= combRad:
				conList.append([currentLocs[i][3],currentLocs[j][3]])
	return conList

def processCons(devoCons, prevCons):
	#adds any new connections to the list and then returns the list
	for devo in devoCons:
		if not (devo in prevCons):
			prevCons.append(devo)

	return prevCons

def makeConnectome(finalConnects,ID,gen,genome):
	# This function takes the list of all the connections that happened and turns that into a
	# list of legal connections in the right sorted order, and a printed verbal output 
	# for the user to read and to be saved in the "Genomes" folder for the generation made

	sortedConnects = []

	verbalOut = ""

	partTypes = ["IR", "Photo", "Neuron", "Right Motor", "Left Motor"]

	#This sorts the connections by their size, so that the first index in any
	# pair is the bigger one. Also if they are the same size in then it puts both 
	# combinations in.
	for i in range(0,len(finalConnects)):
		size1 = genome[finalConnects[i][0]][5] * genome[finalConnects[i][0]][6]
		size2 = genome[finalConnects[i][1]][5] * genome[finalConnects[i][1]][6]
		if size1 > size2:
			sortedConnects.append(finalConnects[i])
		elif size2 > size1:
			sortedConnects.append([finalConnects[i][1],finalConnects[i][0]])
		else:
			sortedConnects.append(finalConnects[i])
			sortedConnects.append([finalConnects[i][1],finalConnects[i][0]])

	length = len(sortedConnects)

	popList = []

	#This makes a list of illegal connections to pop
	for i in range(0,length):
		#Nothing can connect to sensors, so if a connection has one in the second position it is out
		if(genome[sortedConnects[i][1]][0] in [0,1]):
			popList.append(i)
		# Motors can't connect to to other motors, and so if there are motors on both sides then this
		# connection will be popped
		elif(genome[sortedConnects[i][0]][0] in [3,4] and genome[sortedConnects[i][1]][0] in [3,4]):
			popList.append(i)

	#Reverses the list so that popping the first things doesn't mess up the indexing of later things
	# that you want to pop
	popList = list(reversed(popList))

	#Pop things we want to remove
	for pop in popList:
		sortedConnects.pop(pop)

	#print "\n"

	for link in sortedConnects:
		#Makes string to fill with data to print
		number = ""
		neuronNum1 = ""
		neuronNum2 = ""
		polarity = ""
		strength = ""

		#If the first thing is an IR then its number is determined by getting the int value of the 
		#angle + 22.5 (45/2) and the divided by 45 to find which of the 8 segemnts it is in.
		if (genome[link[0]][0] == 0):
			number = str(int((genome[link[0]][1]+22.5) / 45) % 8)

		#Photos work bascially the same way but there isn't the 22.5 degree offset
		elif (genome[link[0]][0] == 1):
			number = str(int(genome[link[0]][1] / 45))

		#The neuron numbers are just their index numbers, no counting
		elif(genome[link[0]][0] == 2):
			neuronNum1 = str(link[0])

		if(genome[link[1]][0] == 2):
			neuronNum2 = str(link[1])

		#The connection strength is negative if the other seed is on the clockwise half,
		# and positive if it's on the widdershins half
		if((genome[link[0]][1] + 180)%360 < genome[link[1]][1]):
			polarity = "-"
		else:
			polarity = "+"

		#Strength is the average of the two distances travaled divided by 250 so that weights are between 0 and 4
		strength = str((genome[link[0]][3] * genome[link[0]][4] + genome[link[1]][3] * genome[link[1]][4]) / 250.0)
 	
 		#Makes the full verbal string
 		#print genome
 		#print int(genome[link[0]][0])
 		#print link[0]
		verbalOut = verbalOut + partTypes[int(genome[link[0]][0])] + " " + number + neuronNum1 + " connects to " + partTypes[genome[link[1]][0]] + " " + neuronNum2
		verbalOut = verbalOut + " with a weight of " + polarity + strength + "\n"

	#print verbalOut

	#Makes a file with the genome and the verbal output
	verbalFile = open("Generation"+str(gen)+"/Genomes/verbose"+ID+".txt","w")
	verbalFile.write(str(genome))
	verbalFile.write("\n \n \n")
	verbalFile.write(verbalOut)
	verbalFile.close()

	# This makes the params.h file and returns 1 if viable
	return makeParams(sortedConnects,ID,gen,genome)

def makeParams(vConnect,ID,gen,genome):
	ardFile = open('Generation'+str(gen)+"/Params/"+'params'+ID+'.h','w')

	#Defines ints and arrays to hold the data for each new param.h, whihc is labeled by ID

	numInputs = 0
	numHidden = 0
	numOutput = 0

	RMILength = 0
	LMILength = 0

	inputIndexes = []
	hiddenIndexes = []
	outputIndexes = []

	senseToInput = []
	inputToHidden = []
	hiddenToHidden = []
	hiddenToOutput = []
	inputToOutput = []
	outputToHidden = []

	RMI = []
	LMI = []

	usedList = []

	#Gets the number of each of hidden, motors and inputs and makes sure there are no duplicates
	# by checkignt he index numbers
	for con in vConnect:
		if not con[0] in usedList:
			if genome[con[0]][0] in [0,1]:
				numInputs = numInputs + 1
				inputIndexes.append(con[0])
			elif genome[con[0]][0] == 2:
				numHidden = numHidden + 1
				hiddenIndexes.append(con[0])
			elif genome[con[0]][0] in [3,4]:
				numOutput = numOutput + 1
				outputIndexes.append(con[0])
			usedList.append(con[0])
		if not con[1] in usedList:
			if genome[con[1]][0] == 2:
				numHidden = numHidden + 1
				hiddenIndexes.append(con[1])
			elif genome[con[1]][0] in [3,4]:
				numOutput = numOutput + 1
				outputIndexes.append(con[1])
			usedList.append(con[1])

	usedList = []

	motorCount = 0
	#Figures out motor indexes and it might look off but there are
	# secret motors who just give output and don't get it
	# print vConnect
	for con in vConnect:
		if not con[1] in usedList or not con[0] in usedList:
			if genome[con[0]][0] == 3:
				motorCount = motorCount + 1
			if genome[con[0]][0] == 4:
				motorCount = motorCount + 1		
			if genome[con[1]][0] == 3:
				RMILength = RMILength + 1
				RMI.append(motorCount)
				motorCount = motorCount + 1
			if genome[con[1]][0] == 4:
				LMILength = LMILength + 1
				LMI.append(motorCount)
				motorCount = motorCount + 1
			usedList.append(con[0])
			usedList.append(con[1])

	usedList = []

	#Figures out which sensor gets which output which is different than their number
	for con in vConnect:
		if not con[0] in usedList:
			if genome[con[0]][0] == 0:
				senseToInput.append(int(((genome[con[0]][1]+22.5) / 45) % 8 )* 2)
			if genome[con[0]][0] == 1:
				senseToInput.append(int((((genome[con[0]][1]) / 45) % 8 )* 2 + 1))
			usedList.append(con[0])

	#makes input to hidden connections and keeps strength at -4 to 4
	# structure is basically the same for each of these things
	for i in range(0,numInputs):
		#makes a list for each input
		perInput = []
		for j in range(0,numHidden):
			#If there is a connection then calcualte the strength and polarity
			if [inputIndexes[i],hiddenIndexes[j]] in vConnect:
				sensor = genome[inputIndexes[i]] 
				hidden = genome[hiddenIndexes[j]]
				strength = (sensor[3] * sensor[4] + hidden[3] * hidden[4]) / 250.0
				if (sensor[1] + 180)%360 < hidden[1]:
					strength = strength * -1
				perInput.append(strength)
			else:
				#Otherwise it is a zero
				perInput.append(0)
		inputToHidden.append(perInput)

	#makes hidden to hidden connections and keeps strength at -4 to 4
	for i in range(0,numHidden):
		perHidden = []
		for j in range(0,numHidden):
			if [hiddenIndexes[i],hiddenIndexes[j]] in vConnect:
				hidden1 = genome[hiddenIndexes[i]] 
				hidden2 = genome[hiddenIndexes[j]]
				strength = (hidden1[3] * hidden1[4] + hidden2[3] * hidden2[4]) / 250.0
				if (hidden1[1] + 180)%360 < hidden2[1]:
					strength = strength * -1
				perHidden.append(strength)
			else:
				perHidden.append(0)
		hiddenToHidden.append(perHidden)

	#makes hidden to output connections and keeps strength at -4 to 4
	for i in range(0,numHidden):
		perHidden = []
		for j in range(0,numOutput):
			if [hiddenIndexes[i],outputIndexes[j]] in vConnect:
				hidden = genome[hiddenIndexes[i]] 
				output = genome[outputIndexes[j]]
				strength = (hidden[3] * hidden[4] + output[3] * output[4]) / 250.0
				if (hidden[1] + 180)%360 < output[1]:
					strength = strength * -1
				perHidden.append(strength)
			else:
				perHidden.append(0)
		hiddenToOutput.append(perHidden)

	#makes input to output connections and keeps strength at -4 to 4
	for i in range(0,numInputs):
		perInput = []
		for j in range(0,numOutput):
			if [inputIndexes[i],outputIndexes[j]] in vConnect:
				sensor = genome[inputIndexes[i]] 
				output = genome[outputIndexes[j]]
				strength = (sensor[3] * sensor[4] + output[3] * output[4]) / 250.0
				if (sensor[1] + 180)%360 < output[1]:
					strength = strength * -1
				perInput.append(strength)
			else:
				perInput.append(0)
		inputToOutput.append(perInput)

	#makes output to hidden connections
	for i in range(0,numOutput):
		perOutput = []
		for j in range(0,numHidden):
			if [outputIndexes[i],hiddenIndexes[j]] in vConnect:
				output = genome[outputIndexes[i]] 
				hidden = genome[hiddenIndexes[j]]
				strength = (output[3] * output[4] + hidden[3] * hidden[4]) / 250.0
				if (output[1] + 180)%360 < hidden[1]:
					strength = strength * -1
				perOutput.append(strength)
			else:
				perOutput.append(0)
		outputToHidden.append(perOutput)

	#can be on robot A to D and arena 1 or 2
	robotVal = random.randint(0,3)
	arenaVal = random.randint(0,1)

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]

	robotVal = robotArray[robotVal]
	arenaVal = arenaArray[arenaVal]

	#writes everything to the params.h file with arrays redone for Arduino C formatting

	ardFile.write("String ID = " + "\""+ ID + "\"; \n")
	ardFile.write('#define NUM_INPUT ' + str(numInputs) + " \n")
	ardFile.write('#define NUM_HIDDEN ' + str(numHidden) + " \n")
	ardFile.write('#define NUM_OUTPUT ' + str(numOutput) + " \n \n")
	ardFile.write("float input[NUM_INPUT]; \n")
	ardFile.write("float hidden[NUM_HIDDEN]; \n")
	ardFile.write("float old_hidden[NUM_HIDDEN]; \n")
	ardFile.write("float output[NUM_OUTPUT]; \n")
	ardFile.write("float old_output[NUM_OUTPUT]; \n \n")
	ardFile.write("const int RMILength = " + str(RMILength) + "; \n")
	ardFile.write("const int LMILength = " + str(LMILength) + "; \n")
	ardFile.write("int RMI[RMILength] = " + str(RMI).replace('[','{').replace(']','}') + "; \n")
	ardFile.write("int LMI[LMILength] = " + str(LMI).replace('[','{').replace(']','}') + "; \n \n")
	ardFile.write("int sensor_to_input[NUM_INPUT] = " + str(senseToInput).replace('[','{').replace(']','}') + "; \n")
	ardFile.write("float input_to_hidden[NUM_INPUT][NUM_HIDDEN] = " + str(inputToHidden).replace('[','{').replace(']','}') + "; \n")
	ardFile.write("float hidden_to_hidden[NUM_HIDDEN][NUM_HIDDEN] = " + str(hiddenToHidden).replace('[','{').replace(']','}') + "; \n")
	ardFile.write("float hidden_to_output[NUM_HIDDEN][NUM_OUTPUT] = " + str(hiddenToOutput).replace('[','{').replace(']','}') + "; \n")
	ardFile.write("float input_to_output[NUM_INPUT][NUM_OUTPUT] = " + str(inputToOutput).replace('[','{').replace(']','}') + "; \n")
	ardFile.write("float output_to_hidden[NUM_OUTPUT][NUM_HIDDEN] = " + str(outputToHidden).replace('[','{').replace(']','}') + "; \n \n \n \n")

	#If there are both motors, and inputs then it is probably viable so return 1
	if 0 in [numInputs,RMILength,LMILength]:
		return 0
	else:
		return 1

def makeNextGen(nextGen):
	#Ok so this is code for making the second and onward generations

	#Opens up the directory of the previous generation
	oldGen = nextGen - 1
	oldGenomes = np.load("Generation"+str(oldGen)+"/Genomes/genomes.npy")

	dirName = "Generation"+str(oldGen)+"/Data/"

	filesNum = len(os.listdir(dirName))

	#get all the data files. THe first is removed as it is just a directory thing here on macs,
	# so that might need to be changed for a different system
	dataFiles = os.listdir(dirName)[1:filesNum]

	sortedData = []
	neededData = 1

	#This sorts the files so that they are accessed by their index order to make sure that the data from the runs \
	# matches up with the genome and ID lists given. 

	while len(dataFiles) > 0:
		for data in dataFiles:
			if(int(data[4:6]) == neededData):
				sortedData.append(data)
				dataFiles.remove(data)
				neededData = neededData + 1

	#print sortedData

	allTimes = []
	allFitnesses = []
	i = 0

	indivFit = []

	for data in sortedData:
		#Here this is to add the "end robot test" at the end as otherwise it just goes off the end
		# and doesn't stop
		w = open(dirName+"/"+data,"a")
		w.write("\n end robot test")
		w.close()
		#Here I open the data file and process the file using processFile()
		f = open(dirName+"/"+data)
		pInfo = processFile(f)
		#This gets the sensor data, number of lines and then timestamps of the data the return 
		# from processFile()
		data = pInfo[0]
		lines = pInfo[1]
		times = pInfo[2]
		#Send the data and line number to calcualte fitness. Time isn't really used here
		fitness = calcFit(data,lines)
		#Save time data and fitness to global varibles
		allTimes.append(times)
		allFitnesses.append(fitness)
		#Return the highest fitness for each, as fitness is fitness at each time step
		indivFit.append(fitness[-1])
		f.close()

	makeOffspring(indivFit,oldGenomes,sortedData,nextGen)

def processFile(f):
	#Defines the arrays that are used for collecting the needed data
	first = True
	dataArray = []
	copyArray = np.zeros(17)
	lineCount = 0
	lastTime = 0
	timeArray = []

	#since each begins with "start robot" this disgregards the first one and then 
	# collects the data from each one after that. In an ideal world you woudl not need this
	# sorting as each file would one have one test's data, but becasue of false starts you
	# can often get extra data
	for line in f:
		if "robot" in line and not first:
			if int(lastTime) > 200000:
				return [dataArray,lineCount,timeArray]
			else:
				dataArray = []
				timeArray = []
				lineCount = 0

		elif "robot" in line:
			first = False

		text = line.split(',')

		if len(text) > 1:
			#adds one more line and copys all the data over to an array which is saved
			lastTime = text[16]
			lineCount = lineCount + 1
			timeArray.append(lastTime)
			for x in range(0,17):
					copyArray[x] = float(text[x])
			dataArray.append(copyArray)
			copyArray = np.zeros(17)

def calcFit(dArray,lineCount):
	areaCount = [0,0,0,0]
	fitTrack = []

	#Finds the means of all the data for photos and IRs
	for data in dArray:
		irMean = np.mean(data[0:16:2])
		photoMean = np.mean(data[1:17:2])

		#returns the count of lines in the different areas based on
		# the means it is given

		areaCount = xorFit(irMean,photoMean,areaCount)

		#The proportions of the two different good zones whihc are used to 
		# calculate fitness

		prop1 = (areaCount[1]/float(lineCount))*100.0
		prop2 = (areaCount[2]/float(lineCount))*100.0

		#fitness calcultion

		multipFit = prop1 + prop2 + ((prop1 * prop2)/10)

		fitTrack.append(multipFit)

	return fitTrack

def xorFit(irVal, photoVal, aCount):
	#IR was 90, photo was 200
	#Threshold values for good and bad regions
	# does a 72% 27% bad/good spilt here, needs tuning 
	# to get 75% 25%
	irThres = 130
	photoThres = 225

	isIRAbove = irVal > irThres
	isPhotoAbove = photoVal > photoThres

	#adjusts the arenaCounts based on the arena the robot was in

	if isIRAbove and isPhotoAbove:
		aCount[0] = aCount[0] + 1
	elif not isIRAbove and not isPhotoAbove:
		aCount[3] = aCount[3] + 1
	elif not isIRAbove and isPhotoAbove:
		aCount[2] = aCount[2] + 1
	elif isIRAbove and not isPhotoAbove:
		aCount[1] = aCount[1] + 1
	
	return aCount

#This function does all the duplication and deletions as well 
# as the muatations

def dupeNmute(genome):
	dupeRate = 0.05
	muteRate = 0.05
	delRate = 0.01
	changePercent = 0.15

	newGenome = []

	firstDupe = True

	#Adds two to the new genome if you get a duplication
	#Adds nothing if there is a deletion

	for gene in genome:
		if random.random() <= dupeRate:
			newGenome.append(list(gene))
			newGenome.append(list(gene))
			#This makes it so having a second duplication after you already had one is more likely
			if firstDupe:
				dupeRate = 0.5
				firstDupe = False
			else:
				dupeRate = dupeRate/2
		else:
			dupeRate = 0.05
			firstDupe = True
		if random.random() > delRate:
			newGenome.append(list(gene))

	#This is the mutation part of the code. The change percent may need to be updated.
	for gene in newGenome:
		for i in range(0,7):
			if random.random() <= muteRate:
				if i == 0:
					gene[i] = random.randint(0,4)
				elif random.random() > 0.5:
					gene[i] = gene[i] + gene[i]*changePercent
				else:
					gene[i] = gene[i] - gene[i]*changePercent
				if i == 1:
					gene[i] = gene[i]%360
	
	#Give the new genes the right kind of ID numbers
	for i in range(0,len(newGenome)):
		newGenome[i][7] = i

	return newGenome

def makeOffspring(indivFit,allGenomes,allIDs,gen):
	#These are the values that determine how many offspring you get
	minOneOff = 30
	minTwoOff = 50
	minThreeOff = 90

	numOffspring = np.zeros(len(indivFit))

	#So this function and array record how many offspring each individual got
	for i in range(0,len(indivFit)):
		if indivFit[i] >= minOneOff and indivFit[i] < minTwoOff:
			numOffspring[i] = 1
		elif indivFit[i] >= minTwoOff and indivFit[i] < minThreeOff:
			numOffspring[i] = 2
		elif indivFit[i] >= minThreeOff:
			numOffspring[i] = 3
		else:
			numOffspring[i] = 0

	#print numOffspring

	#For storing the new generation of genomes and IDs
	newIDs = []
	newGenomes = []

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]

	#print allIDs
	for i in range(0,len(numOffspring)):
		childNumber = 0
		while numOffspring[i] > 0:
			#These two say whihc robot and in whihc area this individual is run
			robotVal = robotArray[random.randint(0,3)]
			arenaVal = arenaArray[random.randint(0,1)]
			#Mutates the right genome and then appends it to the list
			newGenomes.append(dupeNmute(allGenomes[i]))
			#Makes the new ID going Gen,Parent,Index,Robot,Arena
			#print allIDs[i][4:6]
			newID = str(gen).zfill(2) + str(allIDs[i][4:6]).zfill(2) + str(childNumber).zfill(2) + robotVal + arenaVal
			newIDs.append(newID)
			#Keeps track of the number of offspring the individual has left and the index number
			numOffspring[i] = numOffspring[i] - 1
			childNumber = childNumber + 1

	genomeFile = open("Generation"+str(gen)+"/Genomes/genomes.txt","w")
	genomeFile.write(str(newGenomes))
	npNewGenomes = np.asarray(newGenomes)
	np.save("Generation"+str(gen)+"/Genomes/genomes",npNewGenomes)

	for i in range(0,len(newIDs)):
		runDevo(newGenomes[i],newIDs[i],gen)

makeGen()


