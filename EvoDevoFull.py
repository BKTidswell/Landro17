import os
import numpy as np
import random
import math

#The README on github expalins most of the functionality of the code from the user side, so this commenting
# will be primarily for editting of the code itself. Big picture it makes folders that have all the evolutionary
# material for privious generations and the one being currently run. For more big picture and knowing how to 
# run and use this I would say check github

#Important Varibles to Change:
# roboAmount: In makeGenOne(), this is the number of robot in the starting pop
# runTime: In runDevo() this says how long it runs for and should be high enough as for the starting gen
#		   things can run for a max of 200 steps, but if it mutated too high this coudl be an issues
# strenDivide: In makeConnectome() and makeParams(). It needs to be the same value in both places and sets
#   		   what the max connection weight can be, which is basically 1000/strenDivide for the starting
#              generation. Currently set to 250. 
# irThres: Sets the threshold for being above or below the IR value for the XOR. Based on the 75/25 split now. 
#          In xorFit() if you need to change it. 
# photoThres: Sets the threshold for being above or below the Photo value for the XOR. Based on the 75/25 split now
#             In xorFit() if you need to change it. 
# dupeRate: This is the rate of duplication per gene in the genome. In dupeNmute()
# secondDupe: This is the rate of duplication per gene in the genome after one duplication already occured. 
#             In dupeNmute().
# muteRate: This is the mutation rate per item in each gene in the genome, so it checked for each item 
#			individually. In dupeNmute().
# delRate: This is the rate of deletion per gene. In dupeNmute().
# changePercent: This is in dupeNmute() and shows the percent change in values. So if the delay time is 
#				 50 and this is .15 then the new value would be 50*1.15 or 57.5
# 
# In makeGenome() there are a bunch of values that specify the max values for the specifics of the gene values
# and you can change them if you decide that they need tweaking 

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

	return count

def makeGenOne():
	allGenomes = []
	allIDs = []

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]

	mean = 10
	sd = 2

	roboAmount = 20

	#This makes all IDs for the first generation
	for x in range(1,1 + roboAmount):
		robotVal = robotArray[random.randint(0,3)]
		arenaVal = arenaArray[random.randint(0,1)]
		#Makes a genome with number of genes on a normal curve
		numGenes = int(np.random.normal(mean,sd,1))
		genome = makeGenome(numGenes)
		allGenomes.append(genome)
		allIDs.append("0100"+str(x).zfill(2)+ robotVal + arenaVal)

	#allGenomes = [[[4, 187, 73, 5, 14, 1, 54, 0], [4, 234, 67, 4, 33, 1, 51, 1], [0, 223, 7, 4, 70, 3, 13, 2], [3, 220, 83, 4, 42, 3, 87, 3], [1, 329, 73, 3, 68, 2, 54, 4], [3, 335, 64, 5, 85, 3, 58, 5], [4, 282, 100, 1, 57, 3, 56, 6], [4, 117, 47, 5, 49, 1, 19, 7], [2, 237, 44, 5, 45, 3, 59, 8], [4, 93, 48, 5, 53, 2, 44, 9], [0, 45, 88, 1, 54, 3, 17, 10]], [[1, 329, 78, 1, 28, 1, 22, 0], [0, 244, 38, 3, 86, 2, 5, 1], [0, 238, 80, 3, 42, 1, 76, 2], [1, 261, 23, 1, 3, 1, 87, 3], [0, 13, 94, 5, 77, 3, 57, 4], [1, 315, 48, 4, 71, 3, 63, 5], [4, 296, 94, 1, 79, 3, 36, 6], [2, 185, 41, 5, 11, 1, 40, 7], [2, 208, 15, 4, 55, 2, 100, 8], [2, 44, 92, 4, 90, 1, 99, 9]], [[1, 56, 54, 3, 3, 2, 51, 0], [0, 68, 11, 3, 39, 1, 81, 1], [0, 238, 33, 5, 21, 1, 81, 2], [0, 300, 42, 2, 40, 2, 9, 3], [4, 69, 19, 2, 94, 1, 65, 4], [3, 238, 7, 3, 66, 2, 27, 5], [3, 140, 68, 3, 76, 1, 83, 6], [1, 275, 74, 2, 87, 1, 18, 7], [4, 6, 69, 2, 22, 3, 62, 8], [1, 217, 35, 1, 92, 3, 9, 9], [3, 121, 25, 5, 89, 1, 96, 10], [0, 344, 16, 5, 36, 3, 99, 11]], [[0, 134, 80, 1, 86, 2, 40, 0], [0, 270, 36, 2, 48, 3, 27, 1], [0, 323, 69, 1, 62, 3, 74, 2], [2, 348, 39, 1, 12, 3, 17, 3], [4, 282, 50, 3, 17, 3, 79, 4], [4, 4, 25, 3, 97, 1, 79, 5], [3, 155, 45, 1, 85, 3, 90, 6]], [[0, 262, 97, 5, 89, 1, 57, 0], [2, 57, 1, 1, 74, 2, 56, 1], [0, 244, 80, 4, 32, 2, 99, 2], [0, 159, 93, 5, 45, 2, 41, 3], [4, 104, 93, 5, 73, 3, 93, 4], [3, 220, 11, 5, 43, 3, 36, 5], [1, 145, 62, 3, 9, 3, 56, 6], [2, 52, 10, 4, 98, 2, 69, 7]], [[1, 202, 88, 4, 8, 2, 83, 0], [0, 162, 82, 1, 65, 2, 29, 1], [4, 22, 79, 1, 88, 2, 59, 2], [2, 8, 94, 4, 50, 2, 26, 3], [4, 333, 6, 4, 42, 2, 42, 4], [3, 304, 91, 4, 30, 2, 63, 5], [4, 41, 74, 2, 73, 3, 85, 6], [2, 351, 55, 1, 38, 1, 72, 7]], [[3, 112, 51, 5, 94, 3, 13, 0], [3, 201, 41, 1, 99, 2, 86, 1], [4, 82, 98, 1, 70, 2, 40, 2], [4, 236, 55, 1, 91, 1, 51, 3], [3, 145, 67, 2, 11, 1, 52, 4], [0, 296, 96, 2, 12, 3, 59, 5], [1, 2, 92, 2, 99, 2, 54, 6], [0, 33, 17, 5, 59, 2, 44, 7]], [[2, 35, 83, 1, 79, 3, 16, 0], [1, 183, 96, 3, 29, 1, 14, 1], [0, 168, 5, 2, 6, 3, 9, 2], [4, 177, 64, 2, 35, 3, 63, 3], [3, 100, 57, 4, 34, 2, 30, 4], [2, 254, 49, 1, 96, 2, 26, 5], [4, 307, 0, 3, 16, 1, 18, 6], [0, 348, 0, 3, 62, 2, 78, 7], [0, 238, 36, 4, 86, 3, 93, 8], [3, 306, 80, 5, 7, 1, 88, 9]], [[2, 104, 0, 2, 59, 1, 69, 0], [0, 246, 23, 5, 83, 2, 39, 1], [0, 155, 34, 4, 11, 1, 52, 2], [4, 281, 71, 1, 15, 3, 76, 3], [1, 89, 72, 1, 52, 3, 30, 4], [0, 297, 10, 1, 18, 1, 84, 5], [3, 14, 86, 3, 20, 1, 68, 6], [2, 125, 0, 1, 94, 2, 72, 7], [3, 23, 27, 2, 64, 1, 2, 8]], [[4, 341, 47, 1, 55, 2, 76, 0], [2, 298, 15, 5, 28, 1, 81, 1], [3, 249, 54, 1, 97, 2, 94, 2], [4, 110, 17, 2, 98, 2, 93, 3], [2, 188, 93, 3, 79, 2, 38, 4], [4, 42, 12, 5, 56, 3, 60, 5], [4, 108, 18, 4, 83, 1, 73, 6], [2, 13, 49, 1, 48, 2, 36, 7], [3, 25, 79, 3, 84, 3, 53, 8], [0, 213, 98, 1, 43, 3, 37, 9]], [[1, 106, 57, 2, 41, 3, 3, 0], [3, 314, 89, 5, 93, 2, 46, 1], [2, 18, 15, 1, 84, 1, 28, 2], [3, 218, 92, 3, 42, 1, 20, 3], [4, 97, 36, 3, 24, 2, 22, 4], [0, 351, 54, 4, 62, 3, 20, 5], [3, 354, 67, 3, 49, 2, 46, 6]], [[2, 255, 42, 5, 41, 3, 62, 0], [0, 165, 98, 5, 82, 1, 78, 1], [2, 274, 66, 3, 73, 2, 13, 2], [4, 105, 6, 2, 94, 2, 19, 3], [1, 279, 79, 1, 18, 2, 78, 4], [4, 221, 63, 2, 9, 3, 23, 5], [2, 198, 36, 2, 12, 1, 44, 6], [4, 245, 61, 2, 100, 2, 90, 7], [4, 316, 43, 2, 11, 3, 55, 8], [4, 288, 29, 4, 97, 2, 34, 9], [2, 73, 84, 5, 98, 2, 99, 10], [1, 16, 3, 1, 19, 2, 56, 11]], [[2, 166, 12, 5, 79, 1, 49, 0], [3, 249, 78, 3, 37, 3, 81, 1], [3, 193, 82, 1, 98, 2, 45, 2], [2, 103, 32, 1, 75, 3, 32, 3], [1, 22, 50, 1, 4, 1, 73, 4], [4, 152, 0, 5, 75, 2, 99, 5], [1, 284, 47, 1, 72, 1, 3, 6], [0, 227, 26, 3, 16, 3, 87, 7], [0, 341, 97, 5, 70, 2, 3, 8], [1, 250, 70, 2, 92, 2, 43, 9], [2, 284, 97, 1, 100, 2, 84, 10], [1, 194, 66, 4, 11, 1, 5, 11]], [[1, 130, 34, 4, 72, 2, 27, 0], [2, 267, 93, 3, 91, 3, 84, 1], [1, 187, 57, 5, 54, 2, 67, 2], [0, 60, 24, 1, 1, 3, 9, 3], [1, 173, 82, 1, 19, 1, 30, 4], [1, 312, 87, 1, 20, 1, 100, 5], [3, 90, 6, 3, 25, 1, 72, 6], [0, 249, 64, 5, 79, 3, 57, 7], [4, 191, 67, 4, 56, 1, 58, 8]], [[3, 51, 63, 1, 86, 3, 30, 0], [0, 283, 15, 4, 66, 2, 65, 1], [4, 124, 74, 2, 51, 2, 75, 2], [1, 336, 12, 1, 81, 1, 58, 3], [3, 210, 93, 4, 76, 3, 58, 4], [1, 80, 38, 2, 39, 1, 49, 5]], [[4, 235, 12, 3, 83, 3, 58, 0], [0, 223, 48, 3, 46, 2, 89, 1], [0, 306, 90, 2, 47, 2, 7, 2], [3, 134, 22, 5, 56, 1, 74, 3], [1, 52, 72, 1, 84, 1, 96, 4], [1, 113, 91, 2, 53, 1, 54, 5], [0, 83, 7, 1, 46, 3, 60, 6], [0, 64, 17, 4, 72, 2, 17, 7]], [[2, 315, 88, 2, 96, 3, 57, 0], [3, 124, 46, 4, 99, 2, 49, 1], [0, 121, 68, 1, 57, 3, 26, 2], [4, 71, 49, 5, 37, 3, 44, 3], [0, 135, 42, 1, 98, 1, 64, 4], [0, 140, 7, 5, 97, 2, 16, 5], [0, 50, 12, 1, 31, 2, 16, 6], [0, 146, 80, 4, 65, 2, 61, 7], [1, 254, 42, 1, 42, 1, 23, 8], [2, 211, 25, 3, 29, 1, 40, 9], [0, 304, 8, 4, 29, 1, 90, 10]], [[3, 312, 30, 5, 55, 3, 84, 0], [1, 309, 99, 3, 51, 3, 61, 1], [4, 78, 10, 1, 33, 2, 61, 2], [4, 180, 8, 3, 92, 2, 5, 3], [4, 26, 50, 2, 19, 3, 11, 4], [0, 100, 32, 3, 26, 1, 54, 5], [0, 218, 83, 1, 90, 1, 23, 6], [1, 224, 63, 3, 41, 3, 10, 7], [2, 136, 10, 3, 73, 2, 66, 8]], [[3, 30, 82, 3, 74, 3, 73, 0], [1, 293, 83, 3, 78, 1, 19, 1], [1, 18, 17, 5, 95, 2, 67, 2], [0, 121, 31, 3, 87, 1, 54, 3], [0, 202, 53, 3, 27, 2, 54, 4], [0, 263, 71, 1, 11, 1, 13, 5], [0, 102, 12, 5, 66, 3, 58, 6], [1, 42, 32, 2, 100, 1, 61, 7]], [[3, 120, 81, 3, 95, 2, 67, 0], [4, 315, 78, 1, 84, 2, 2, 1], [3, 145, 97, 4, 22, 2, 71, 2], [2, 149, 67, 4, 9, 2, 78, 3], [1, 245, 81, 1, 71, 3, 77, 4], [1, 124, 65, 3, 34, 2, 92, 5]]]

	#This writes a human readable genome and an numpy readable genome into the genomes folder
	genomeFile = open("Generation1/Genomes/genomes.txt","w")
	genomeFile.write(str(allGenomes))
	npGenomes = np.asarray(allGenomes)
	np.save("Generation1/Genomes/genomes",npGenomes)
	#print allIDs

	gen = 1

	#runs the devlopment and connections for each robot in the generation
	for i in range(0,len(allIDs)):
		runDevo(allGenomes[i],allIDs[i],gen)


def makeGenome(nGenes):
	maxSpawn = 100
	maxgSpawn = 100
	vMax = 100
	vDurationMax = 100
	gMax = 100
	gDurationMax = 100
	maxAngle = 360

	# 0 = Part Type (0 = IR, 1 = Photo, 2 = Neuron, 3 = R Motor, 4 = L Motor)
	# 1 = Angle
	# 2 = Spawn Time
	# 3 = Velocity
	# 4 = Travel Time
	# 5 = Start Growth Time
	# 6 = Growth Rate 
	# 7 = Growth Time
	# 8 = Index

	genome = [[0 for x in range(9)] for y in range(nGenes)] 

	for i in range(0,nGenes):
		genome[i][0] = random.randint(0,4)
		genome[i][1] = random.randint(0,maxAngle)
		genome[i][2] = random.randint(0,maxSpawn)
		genome[i][3] = random.randint(0,vMax)
		genome[i][4] = random.randint(0,vDurationMax)
		genome[i][5] = random.randint(0,maxgSpawn)
		genome[i][6] = random.randint(1,gMax)
		genome[i][7] = random.randint(1,gDurationMax)
		genome[i][8] = i

	return genome

def runDevo(genome,ID,gen):

	count = 0
	connects = []

	#no longer makes an image but just runs trhough the step processes
	#1000 was picked with the idea that it would take a while for the devlopment
	#time to take that long.
	runTime = 1000
	while count < runTime:
		#ProcessCons is run on the connections found on each cycle and updates
		#the connection list so that there are no duplicates
		connects = processCons(devoGraphics(genome, count), connects)
		count = count + 1

	#Returns 0 if it's not viable and 1 if it is (or probably is)
	return makeConnectome(connects,ID,gen,genome)

def devoGraphics(genome, count):

	center = [500,500]

	irPointList = []
	photoPointList = []

	genePosList = []

	currentList = []

	#Moves it using X and Y from the center
	for gene in genome:
		if gene[2] <= count:
			#Runs based on the count
			if gene[4]+gene[2] >= count:
				x = center[0] + gene[3]*(count-gene[2])*math.cos(math.radians(gene[1]))
				y = center[1] + gene[3]*(count-gene[2])*math.sin(math.radians(gene[1]))
			#If it has run for it's full development time then it stops moving
			else:
				x = center[0] + gene[3]*gene[4]*math.cos(math.radians(gene[1]))
				y = center[1] + gene[3]*gene[4]*math.sin(math.radians(gene[1]))

		#Grows based on count if the growth delay has passed
		if gene[2] + gene[5] <= count:
			if gene[7]+gene[5]+gene[2] >= count:
					size = 1+gene[6]*(count-gene[2]-gene[5])
			#Again if it is past the growth time then it stops growing
			else:
				size = 1+gene[6]*gene[7]

		#Only adds it to the list if it has moved and has a size
		if gene[2] <= count and gene[2] + gene[5] <= count:
			currentList.append([x,y,size,gene[8]])
	
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

	strenDivide = 250.0

	#This sorts the connections by their size, so that the first index in any
	# pair is the bigger one. Also if they are the same size in then it puts both 
	# combinations in.
	for i in range(0,len(finalConnects)):
		size1 = genome[finalConnects[i][0]][6] * genome[finalConnects[i][0]][7]
		size2 = genome[finalConnects[i][1]][6] * genome[finalConnects[i][1]][7]
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
		motorNum1 = ""
		motorNum2 = ""

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

		if genome[link[0]][0] in [3,4]:
			motorNum1 = str(genome[link[0]][8])

		if genome[link[1]][0] in [3,4]:
			motorNum2 = str(genome[link[1]][8])

		#Strength is the average of the two distances travaled divided by 250 so that weights are between 0 and 4
		strength = str((genome[link[0]][3] * genome[link[0]][4] + genome[link[1]][3] * genome[link[1]][4]) / strenDivide)
 	
 		#Makes the full verbal string
 		#print genome
 		#print int(genome[link[0]][0])
 		#print link[0]
		if genome[link[0]][0] in [2,3,4]:
			firstSTR = str(genome[link[0]][8])
		else:
			firstSTR = ""

		verbalOut = verbalOut + partTypes[genome[link[0]][0]] + " " + firstSTR + number + " connects to " 
		verbalOut = verbalOut + partTypes[genome[link[1]][0]] + " " + str(genome[link[1]][8]) +  " with a weight of " + polarity + strength + "\n"


	#print verbalOut

	#Makes a file with the genome and the verbal output
	verbalFile = open("Generation"+str(gen)+"/Genomes/verbose"+ID+".txt","w")
	verbalFile.write(str(genome))
	verbalFile.write("\n \n \n")
	verbalFile.write(verbalOut)
	if len(sortedConnects) == 0:
		verbalFile.write("There were no connections made") 
	verbalFile.close()

	# This makes the params.h file and returns 1 if viable
	return makeParams(sortedConnects,ID,gen,genome)

def makeParams(vConnect,ID,gen,genome):
	ardFile = open('Generation'+str(gen)+"/Params/"+'params'+ID+'.h','w')

	#Defines ints and arrays to hold the data for each new param.h, whihc is labeled by ID

	strenDivide = 250.0

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
		if not con[0] in usedList:
			if genome[con[0]][0] == 3:
				RMILength = RMILength + 1
				RMI.append(motorCount)
				motorCount = motorCount + 1
			if genome[con[0]][0] == 4:
				LMILength = LMILength + 1
				LMI.append(motorCount)
				motorCount = motorCount + 1
			usedList.append(con[0])
		if not con[1] in usedList:
			if genome[con[1]][0] == 3:
				RMILength = RMILength + 1
				RMI.append(motorCount)
				motorCount = motorCount + 1
			if genome[con[1]][0] == 4:
				LMILength = LMILength + 1
				LMI.append(motorCount)
				motorCount = motorCount + 1
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
				strength = (sensor[3] * sensor[4] + hidden[3] * hidden[4]) / strenDivide
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
				strength = (hidden1[3] * hidden1[4] + hidden2[3] * hidden2[4]) / strenDivide
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
				strength = (hidden[3] * hidden[4] + output[3] * output[4]) / strenDivide
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
				strength = (sensor[3] * sensor[4] + output[3] * output[4]) / strenDivide
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
				strength = (output[3] * output[4] + hidden[3] * hidden[4]) / strenDivide
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
	neededData = 0

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

	#print fitTrack[-1]

	# print areaCount
	# print prop1
	# print prop2
	# print fitTrack[-1]

	return fitTrack

def xorFit(irVal, photoVal, aCount):
	#IR was 90, photo was 200
	#Threshold values for good and bad regions
	# does a 43% 57% bad/good spilt here, but each good bad area is the same
	irThres = 49
	photoThres = 126

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
	secondDupe = 0.5

	angleRange = 360
	processRange = 100

	newGenome = []

	firstDupe = True

	for gene in genome:
		if random.random() <= dupeRate:
			newGenome.append(list(gene))
			newGenome.append(list(gene))
			if firstDupe:
				dupeRate = secondDupe
			else:
				dupeRate = dupeRate/2
		else:
			newGenome.append(list(gene))
			dupeRate = 0.05
			firstDupe = False

	for gene in newGenome:
		if random.random() <= delRate:
			newGenome.pop(newGenome.index(gene))

	for gene in newGenome:
		for i in range(0,7):
			if random.random() <= muteRate:
				if i == 0:
					gene[i] = random.randint(0,4)
				elif i == 1:
					gene[i] = random.randrange(0,angleRange)
				else:
					gene[i] = random.randrange(0,processRange)

	
	for i in range(0,len(newGenome)):
		newGenome[i][7] = i

	return newGenome

def makeOffspring(indivFit,allGenomes,allIDs,gen):
	#These are the values that determine how many offspring you get

	numOffspring = np.zeros(len(indivFit))

	#So this function and array record how many offspring each individual got
	for i in range(0,len(indivFit)):
		numOffspring[i] = fitFunc(indivFit[i],len(allGenomes))
		
	#For storing the new generation of genomes and IDs
	newIDs = []
	newGenomes = []

	robotArray = ["A","B","C","D"]
	arenaArray = ["1","2"]


	for i in range(0,len(numOffspring)):
		childNumber = 1
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


def fitFunc(fit,popSize):
	base = 0.3
	highChance = 0.5
	mod = popSize
	if fit < 20+mod and random.random() < base:
		return 1
	elif fit >= 20+mod and fit < 30+mod and random.random() < (base + 0.1):
		return 1
	elif fit >= 30+mod and fit < 40+mod and random.random() < (base + 0.2):
		return 1
	# elif fit >= 40 and fit < 50 and random.random() < (base + 0.3):
	# 	return 1
	elif fit >= 40+mod and fit < 70+mod:
		return 1
	# elif fit >= 80 and random.random() < highChance:
	# 	return 2
	elif fit >= 70+mod:
		return 2
	else:
		return 0


genNumb = makeGen()
if genNumb != 1:
	dataPath = "Generation"+str(genNumb-1)+"/Data/"
	numbData = len(os.listdir(dataPath))
	if numbData > 1:
		print "Successfully Created Generation " + str(genNumb)
	else:
		print "Please Add Datalogs to " + dataPath
		os.rmdir("Generation"+str(genNumb)+"/Data/")
		os.rmdir("Generation"+str(genNumb)+"/Params/")
		os.remove("Generation"+str(genNumb)+"/Genomes/genomes.npy")
		os.remove("Generation"+str(genNumb)+"/Genomes/genomes.txt")
		os.rmdir("Generation"+str(genNumb)+"/Genomes/")
		os.rmdir("Generation"+str(genNumb))
else:
	print "Successfully Created Generation " + str(genNumb)


