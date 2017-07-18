import os
import numpy as np
import random
import math

def makeGen():
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

	for x in range(1,1+5):
		robotVal = robotArray[random.randint(0,3)]
		arenaVal = arenaArray[random.randint(0,1)]
		numGenes = int(np.random.normal(mean,sd,1))
		genome = makeGenome(numGenes)
		allGenomes.append(genome)
		allIDs.append("0100"+str(x).zfill(2)+ robotVal + arenaVal)

	genomeFile = open("Generation1/Genomes/genomes.txt","w")
	genomeFile.write(str(allGenomes))
	allGenomes = np.asarray(allGenomes)
	np.save("Generation1/Genomes/genomes",allGenomes)
	print allIDs

	gen = 1

	for i in range(0,len(allIDs)):
		runDevo(allGenomes[i],allIDs[i],gen)


def makeGenome(nGenes):
	maxSpawn = 100
	vMax = 5
	vDurationMin = 1
	vDurationMax = 100
	gMax = 3
	gDurationMin = 1
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

	# display = 750 x 650
	count = 0
	connects = []

	while count < 500:
		processCons(devoGraphics(genome, count), connects)
		count = count + 1

	return makeConnectome(connects,ID,gen,genome)

def devoGraphics(genome, count):

	center = [375,325]

	irPointList = []
	photoPointList = []
	pointRad = 3

	genePosList = []

	currentList = []

	for gene in genome:
		if gene[2] <= count:
			if gene[4]+gene[2] >= count:
				x = int(center[0] + gene[3]*(count-gene[2])*math.cos(math.radians(gene[1])))
				y = int(center[1] + gene[3]*(count-gene[2])*math.sin(math.radians(gene[1])))
			else:
				x = int(center[0] + gene[3]*gene[4]*math.cos(math.radians(gene[1])))
				y = int(center[1] + gene[3]*gene[4]*math.sin(math.radians(gene[1])))

			if gene[6]+gene[2] >= count:
				size = int(1+gene[5]*(count-gene[2]))
			else:
				size = int(1+gene[5]*gene[6])

			currentList.append([x,y,size,gene[7]])
			
	return checkConds(currentList)

def distance(x1,x2,y1,y2):
	return (math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def checkConds(currentLocs):
	conList = [] 

	for i in range(0,len(currentLocs)-1):
		for j in range(i+1,len(currentLocs)):
			dist = distance(currentLocs[i][0],currentLocs[j][0],currentLocs[i][1],currentLocs[j][1])
			combRad = currentLocs[i][2] + currentLocs[j][2]
			if dist <= combRad:
				conList.append([currentLocs[i][3],currentLocs[j][3]])
	return conList

def processCons(devoCons, prevCons):
	for dev in devoCons:
		if not (dev in prevCons):
			prevCons.append(dev)

	return prevCons

def makeConnectome(finalConnects,ID,gen,genome):
	sortedConnects = []

	verbalOut = ""

	partTypes = ["IR", "Photo", "Neuron", "Right Motor", "Left Motor"]

	# for gene in genome:
	#     print partTypes[gene[0]]

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

	#print "\n"
	#print sortedConnects

	length = len(sortedConnects)

	popList = []

	for i in range(0,length):
		if(genome[sortedConnects[i][1]][0] in [0,1]):
			popList.append(i)
		elif(genome[sortedConnects[i][0]][0] in [3,4] and genome[sortedConnects[i][1]][0] in [3,4]):
			popList.append(i)

	popList = list(reversed(popList))

	#print popList

	for pop in popList:
		sortedConnects.pop(pop)

	#print "\n"
	#print sortedConnects

	print "\n"

	for link in sortedConnects:
		number = ""
		neuronNum1 = ""
		neuronNum2 = ""
		polarity = ""
		strength = ""

		if (genome[link[0]][0] == 0):
			number = str(int((genome[link[0]][1]+22.5) / 45) % 8)

		elif (genome[link[0]][0] == 1):
			number = str(int(genome[link[0]][1] / 45))

		elif(genome[link[0]][0] == 2):
			neuronNum1 = str(link[0])

		if(genome[link[1]][0] == 2):
			neuronNum2 = str(link[1])

		if((genome[link[0]][1] + 180)%360 < genome[link[1]][1]):
			polarity = "-"
		else:
			polarity = "+"

		strength = str((genome[link[0]][3] * genome[link[0]][4] + genome[link[1]][3] * genome[link[1]][4]) / 250.0)
 
		verbalOut = verbalOut + partTypes[int(genome[link[0]][0])] + " " + number + neuronNum1 + " connects to " + partTypes[genome[link[1]][0]] + " " + neuronNum2
		verbalOut = verbalOut + " with a weight of " + polarity + strength + "\n"

	print verbalOut

	verbalFile = open("Generation"+str(gen)+"/Genomes/verbose"+ID+".txt","w")
	verbalFile.write(verbalOut)
	verbalFile.close()

	return makeParams(sortedConnects,ID,gen,genome)

def makeParams(vConnect,ID,gen,genome):
	ardFile = open('Generation'+str(gen)+"/Params/"+'params'+ID+'.h','w')

	#print vConnect

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

	#Gets the number of each
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
	#Figures out motor indexes
	print vConnect
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

	#Figures out which sensor gets which output
	for con in vConnect:
		if not con[0] in usedList:
			if genome[con[0]][0] == 0:
				senseToInput.append(int(((genome[con[0]][1]+22.5) / 45) % 8 )* 2)
			if genome[con[0]][0] == 1:
				senseToInput.append(int((((genome[con[0]][1]) / 45) % 8 )* 2 + 1))
			usedList.append(con[0])

	#makes input to hidden connections
	for i in range(0,numInputs):
		perInput = []
		for j in range(0,numHidden):
			if [inputIndexes[i],hiddenIndexes[j]] in vConnect:
				sensor = genome[inputIndexes[i]] 
				hidden = genome[hiddenIndexes[j]]
				strength = (sensor[3] * sensor[4] + hidden[3] * hidden[4]) / 250.0
				if (sensor[1] + 180)%360 < hidden[1]:
					strength = strength * -1
				perInput.append(strength)
			else:
				perInput.append(0)
		inputToHidden.append(perInput)

	#makes hidden to hidden connections
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

	#makes hidden to output connections
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

	#makes input to output connections
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

	robotVal = random.randint(0,3)
	arenaVal = random.randint(0,1)

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]

	robotVal = robotArray[robotVal]
	arenaVal = arenaArray[arenaVal]

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

	if 0 in [numInputs,RMILength,LMILength]:
		return 0
	else:
		return 1

def makeNextGen(nextGen):
	oldGen = nextGen - 1
	oldGenomes = np.load("Generation"+str(oldGen)+"/Genomes/genomes.npy")

	dirName = "Generation"+str(oldGen)+"/Data/"

	filesNum = len(os.listdir(dirName))

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

	print sortedData

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

	print numOffspring

	#For storing the new generation of genomes and IDs
	newIDs = []
	newGenomes = []

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]

	print allIDs
	for i in range(0,len(numOffspring)):
		childNumber = 0
		while numOffspring[i] > 0:
			#These two say whihc robot and in whihc area this individual is run
			robotVal = robotArray[random.randint(0,3)]
			arenaVal = arenaArray[random.randint(0,1)]
			#Mutates the right genome and then appends it to the list
			newGenomes.append(dupeNmute(allGenomes[i]))
			#Makes the new ID going Gen,Parent,Index,Robot,Arena
			print allIDs[i][4:6]
			newID = str(gen).zfill(2) + str(allIDs[i][4:6]).zfill(2) + str(childNumber).zfill(2) + robotVal + arenaVal
			newIDs.append(newID)
			#Keeps track of the number of offspring the individual has left and the index number
			numOffspring[i] = numOffspring[i] - 1
			childNumber = childNumber + 1

	genomeFile = open("Generation"+str(gen)+"/Genomes/genomes.txt","w")
	genomeFile.write(str(newGenomes))
	newGenomes = np.asarray(newGenomes)
	np.save("Generation"+str(gen)+"/Genomes/genomes",newGenomes)

	for i in range(0,len(newIDs)):
		runDevo(newGenomes[i],newIDs[i],gen)

makeGen()


