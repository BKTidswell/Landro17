import os
import numpy as np
import random 

#gen = input("Please Input Generation Number")

#Gen, allGenomes, and allIDs will be input by the user and will have been given by the Params.h maker program for
# ease of copy and pasting.

gen = 5

allGenomes = [[[0, 137, 72, 1, 57, 3.45, 10.35, 0], [0, 6, 71, 1, 80, 2, 7, 1], [0, 209, 12, 3, 22, 3, 51, 2], [3, 39, 38, 4, 53, 1, 23, 3], [4, 357, 33.35, 5, 30, 3, 91, 4], [1, 339, 47, 4, 76, 2, 69, 5], [4, 205, 2, 5, 93, 1, 44, 6], [2, 195, 90, 1, 71, 1, 98, 7], [3, 42, 55, 4, 62, 1, 43, 8], [4, 289, 18.7, 4, 54, 2, 43, 9], [1, 288, 92, 2, 64, 2, 53, 10]],
			  [[0, 359, 87, 3, 77, 1, 33, 0], [0, 236, 58, 1.15, 30, 3, 29, 1], [0, 236, 58, 1, 30, 3, 29, 2], [0, 236, 58, 1, 30, 3, 29, 3], [2, 274, 24, 1, 60, 2, 83, 4], [1, 12.65, 14, 3, 68, 2, 80, 5], [3, 17, 18, 3, 25, 1, 8, 6], [4, 53, 46, 4, 15, 3, 3, 7], [4, 145, 30, 4.25, 23, 1, 71.4, 8], [4, 145, 30, 5, 23, 1, 84, 9], [4, 145, 30, 5, 23, 1, 96.6, 10], [2, 80, 52, 5, 22, 2, 80, 11], [0, 258, 95, 1, 24, 3, 41.65, 12], [1, 45, 28, 5, 18, 2, 92, 13]],
			  [[0, 94, 35, 2, 93, 3, 71, 0], [3, 55, 28, 5, 96, 1, 87, 1], [2, 72, 63, 1, 16, 1, 94, 2], [0, 80, 65, 3, 30, 1, 58, 3], [4, 124, 65, 1, 76, 1, 25, 4], [4, 124, 65, 1, 76, 1, 25, 5], [4, 124, 65, 1, 76, 1, 25, 6], [3, 73, 18, 4, 71, 3, 49, 7], [1, 350, 21, 5, 92, 1, 89, 8], [0, 260, 100, 4, 7, 3, 4, 9], [3, 321, 25, 1, 78, 3, 29, 10]],
			  [[0, 103, 79, 1, 65, 3, 55, 0], [2, 329, 0, 1, 52, 1, 91, 1], [1, 284, 16, 2, 29, 3, 15, 2], [4, 274, 70, 2, 69, 1, 41, 3], [4, 280, 15, 2, 80, 1, 79, 4], [2, 218, 14, 1, 86, 1, 55, 5], [0, 194, 74, 4, 51, 2, 76, 6], [4, 107, 56, 4, 93, 2, 53, 7], [1, 302, 55, 1, 49, 3, 28, 8], [3, 76, 58, 1, 98, 3, 20, 9]],
			  [[1, 210, 91, 4, 26, 3, 33, 0], [4, 224, 34, 1, 29, 3, 40, 1], [3, 220, 29, 5, 4, 1, 51, 2], [1, 202, 13, 2, 27, 2, 100, 3], [2, 188, 70, 5, 12, 2, 27, 4], [1, 320, 99, 4, 3, 1, 94, 5], [0, 345, 49, 1, 18, 3, 78, 6], [0, 238, 13, 5, 31, 2, 79.9, 7], [3, 3, 54, 4, 2, 2, 52, 8], [1, 55, 91, 5, 56, 3, 25, 9], [1, 67, 69, 3, 96, 3, 1, 10]]]

allIDs = ["040100A2","040201C21","040102D1","040503B2","040504A1"]

#This finds the files in the directory of the appropriate directory

dirName = "Generation"+str(gen)

filesNum = len(os.listdir(dirName))

dataFiles = os.listdir(dirName)[1:filesNum]

sortedData = []
neededData = 0

#This sorts the files so that they are accessed by their index order to make sure that the data from the runs \
# matches up with the genome and ID lists given. 

while len(dataFiles) > 0:
	for data in dataFiles:
		if(int(data[4:6]) == neededData):
			sortedData.append(data)
			dataFiles.remove(data)
			neededData = neededData + 1


print sortedData

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
	irThres = 150
	photoThres = 200

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


#Ok so this is the bit of code that runs everything

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

print indivFit

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

for i in range(0,len(numOffspring)):
	childNumber = 0
	while numOffspring[i] > 0:
		#These two say whihc robot and in whihc area this individual is run
		robotVal = robotArray[random.randint(0,3)]
		arenaVal = arenaArray[random.randint(0,1)]
		#Mutates the right genome and then appends it to the list
		newGenomes.append(dupeNmute(allGenomes[i]))
		#Makes the new ID going Gen,Parent,Index,Robot,Arena
		newID = str(gen).zfill(2) + str(allIDs[i][4:6]).zfill(2) + str(childNumber).zfill(2) + robotVal + arenaVal
		newIDs.append(newID)
		#Keeps track of the number of offspring the individual has left and the index number
		numOffspring[i] = numOffspring[i] - 1
		childNumber = childNumber + 1

print newIDs
print newGenomes
	







