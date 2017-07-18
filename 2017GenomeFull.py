#Quick Genome Maker


# imports all the needed python libraries
import time
import random
import pygame, sys
from pygame.locals import *
import math
import numpy
import plotly.plotly as py
from plotly.graph_objs import *
import plotly
import igraph as ig
import networkx as nx

# creates the display for the pygame window
global DISPLAY

DISPLAY=pygame.display.set_mode((750,650))

numGenes = 10

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
def makeGenome(nGenes):
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

#genome = [[1,359,0,3,50,6,20,0],[2,45,0,3,50,5,20,1],[4,325,0,3,50,4,20,2]]


#print genome 

def runDevo(genome):

	# display = 750 x 650

	pygame.init()

	WHITE=(255,255,255)

	DISPLAY.fill(WHITE)

	count = 0
	connects = []

	while count < 225:
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
				#print connects

		time.sleep(0.15)
		DISPLAY.fill((255, 255, 255))
		connects = processCons(devoGraphics(genome, count), connects)
		pygame.display.update()
		count = count + 1

	pygame.display.update()
	pygame.image.save(DISPLAY, 'Devo')
	return makeConnectome(connects)   

def devoGraphics(genome, count):

	center = [375,325]

	irPointList = []
	photoPointList = []
	pointRad = 3

	genePosList = []

	currentList = []

	alpha = 0

	irColor = (255,0,0,alpha) #red
	pColor = (255,233,0,alpha) #yellow
	nColor = (42,198,39,alpha) #green
	rmColor = (25,53,214,alpha) #blue
	lmColor = (163,25,214,alpha) #purple

	colorArray = [irColor,pColor,nColor,rmColor,lmColor]

	pygame.draw.circle(DISPLAY,irColor,[375+250,325],10,10)

	for x in range(0,16,2):
		irPointList.append([int(375+250*math.cos(0.78539816*x/2)),int(325+250*math.sin(0.78539816*x/2))])

	for place in irPointList:
		pygame.draw.circle(DISPLAY,irColor,place,3,3)

	for x in range(1,17,2):
		photoPointList.append([int(375+250*math.cos(0.78539816*x/2)),int(325+250*math.sin(0.78539816*x/2))])

	for place in photoPointList:
		pygame.draw.circle(DISPLAY,pColor,place,3,3)

	# 0 = Part Type (0 = IR, 1 = Photo, 2 = Neuron, 3 = R Motor, 4 = L Motor)
	# 1 = Angle
	# 2 = Start Time
	# 3 = Velocity
	# 4 = Travel Time
	# 5 = Growth Rate
	# 6 = Growth Time

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

			color = colorArray[gene[0]]

			pygame.draw.circle(DISPLAY,color,[x,y],size,1)

	return checkConds(currentList)

def distance(x1,x2,y1,y2):
	return (math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

def checkConds(currentLocs):
	#print currentLocs
	conList = [] 

	for i in range(0,len(currentLocs)-1):
		for j in range(i+1,len(currentLocs)):
			dist = distance(currentLocs[i][0],currentLocs[j][0],currentLocs[i][1],currentLocs[j][1])
			combRad = currentLocs[i][2] + currentLocs[j][2]
			if dist <= combRad:
				conList.append([currentLocs[i][3],currentLocs[j][3]])
				#print [currentLocs[i][3],currentLocs[j][3]]
	return conList
			

def processCons(devoCons, prevCons):
	# print "some connects"
	# print devoCons
	# print prevCons
	for dev in devoCons:
		if not (dev in prevCons):
			prevCons.append(dev)

	return prevCons

	# 0 = Part Type (0 = IR, 1 = Photo, 2 = Neuron, 3 = R Motor, 4 = L Motor)
	# 1 = Angle
	# 2 = Start Time
	# 3 = Velocity
	# 4 = Travel Time
	# 5 = Growth Rate
	# 6 = Growth Time

def makeConnectome(finalConnects):
	# print "final"
	# print finalConnects
	
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

	# print "\n"
	# print "sorted"
	# print sortedConnects

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
 
		verbalOut = verbalOut + partTypes[genome[link[0]][0]] + " " + number + neuronNum1 + " connects to " + partTypes[genome[link[1]][0]] + " " + neuronNum2
		verbalOut = verbalOut + " with a weight of " + polarity + strength + "\n"

	print verbalOut

	return makeParams(sortedConnects)

def makeParams(vConnect):
	ardFile = open('params.h','w')

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

	ardFile.write("String ROBOT = " + "\""+ robotVal + "\"; \n")
	ardFile.write("String ARENA = " + "\""+ arenaVal + "\"; \n \n")
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
		#modul(vConnect)
		return 1


def modul(Edges):
	edgeNodes = []

	for i in range(0,len(Edges)):
		for j in range(0,2):
			if Edges[i][j] not in edgeNodes:
				edgeNodes.append(Edges[i][j])

	if len(edgeNodes) == 0:
		return False

	N = len(edgeNodes)

	newEdges = []

	for e in Edges:
		newEdges.append([edgeNodes.index(e[0]),edgeNodes.index(e[1])])

	oldEdges = Edges
	Edges = newEdges

	G=ig.Graph(Edges, directed=False)

	labels=[]
	group=[]

	for i in edgeNodes:
		if (genome[i][0] == 0):
			lab = "IR " + str(int((genome[i][1]+22.5) / 45) % 8)
		elif (genome[i][0] == 1):
			lab = "Photo " + str(int(genome[i][1] / 45))
		elif(genome[i][0] == 2):
			lab = "Neuron " + str(genome[i][7])
		elif(genome[i][0] == 3):
			lab = "Right Motor"
		elif(genome[i][0] == 4):
			lab = "Left Motor"
		labels.append(lab)
		group.append(i)

	weights = []
	for e in oldEdges:
		if((genome[e[0]][1] + 180)%360 < genome[e[1]][1]):
			polarity = "-"
		else:
			polarity = "+"

		strength = str((genome[e[0]][3] * genome[e[0]][4] + genome[e[1]][3] * genome[e[1]][4]) / 100.0)

		weights.append(polarity + strength)

	layt=G.layout('kk', dim=3)

	Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
	Yn=[layt[k][1] for k in range(N)]# y-coordinates
	Zn=[layt[k][2] for k in range(N)]# z-coordinates
	Xe=[]
	Ye=[]
	Ze=[]

	for e in Edges:
	    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
	    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
	    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

	trace1=Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               #text = weights,
               hoverinfo='none')
	trace2=Scatter3d(x=Xn,
	               y=Yn,
	               z=Zn,
	               mode='markers',
	               name='actors',
	               marker=Marker(symbol='dot',
	                             size=6,
	                             color=group,
	                             colorscale='Rainbow',
	                             line=Line(color='rgb(0,0,0)', width=1)),
	               text=labels,
	               hoverinfo='text')

	axis=dict(showbackground=False,
	          showline=False,
	          zeroline=False,
	          showgrid=False,
	          showticklabels=False,
	          title='')

	layout = Layout(
         title="Network",
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),),
	     margin=Margin(
	        t=100),
	    hovermode='closest',
	    annotations=Annotations([
	           Annotation(
	           showarrow=False,
	            xref='paper',
	            yref='paper',
	            x=0,
	            y=0.1,
	            xanchor='left',
	            yanchor='bottom',
	            font=Font(
	            size=14))]),)

	data=Data([trace1, trace2])
	fig=Figure(data=data, layout=layout)

	plotly.offline.plot(fig, filename='Network.html')

def dupeNmute(genome):
	dupeRate = 0.05
	muteRate = 0.05
	delRate = 0.01
	changePercent = 0.15

	newGenome = []

	firstDupe = True

	for gene in genome:
		if random.random() <= dupeRate:
			newGenome.append(list(gene))
			newGenome.append(list(gene))
			if firstDupe:
				dupeRate = 0.5
			else:
				dupeRate = dupeRate/2
		else:
			dupeRate = 0.05
			firstDupe = False
		if random.random() > delRate:
			newGenome.append(list(gene))

	for gene in newGenome:
		for i in range(0,7):
			if random.random() <= muteRate:
				if i == 0:
					gene[i] = random.randint(0,4)
				elif random.random() > 0.5:
					gene[i] = gene[i] + gene[i]*changePercent
				else:
					gene[i] = gene[i] - gene[i]*changePercent
	
	for i in range(0,len(newGenome)):
		newGenome[i][7] = i

	print(newGenome)

	return newGenome



mean = 10
sd = 2
numGenes = int(numpy.random.normal(mean,sd,1))
genome = makeGenome(6)
#print runDevo(genome)
#genome = [[2, 170, 97, 2, 22, 2, 80, 0], [3, 209, 74, 4, 11, 2, 65, 1], [1, 263, 71, 5, 85, 1, 19, 2], [1, 4, 48, 5, 45, 2, 91, 3], [0, 58, 12, 1, 75, 3, 66, 4], [0, 37, 11, 5, 44, 1, 82, 5]]
print genome
#genome = dupeNmute(genome)
print runDevo(genome)

# viableNums = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# for i in range(0,20):
#     numGenes = i+1
#     print numGenes
#     for j in range(0,1000):
#         genome = makeGenome(numGenes)
#         viableNums[i] = viableNums[i] + runDevo(genome)

#[[4, 326, 49, 2, 31, 2, 20, 0], [2, 70, 73, 4, 19, 3, 85, 1], [2, 262, 89, 4, 3, 2, 8, 2], [0, 157, 32, 4, 4, 2, 72, 3], [2, 103, 69, 5, 70, 2, 17, 4], [0, 3, 33, 3, 39, 2, 89, 5]]


# print viableNums

#Num genes 4,5,6,7,8,9,10,11,12
#[2, 3, 15, 18, 38, 42, 36, 62, 68] out of 100
#[36, 87, 145, 241, 304, 394, 458, 572, 664] out of 1000
#[0, 0, 15, 27, 84, 154, 223, 313, 388, 507, 555, 627, 704, 770, 827, 849, 880, 892, 922, 935] out of 1000

