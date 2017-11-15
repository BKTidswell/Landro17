import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import random
import numpy as np


def genBimodal():
	if(random.random() < highPer):
		mean = 62
		sd = 10
	else:
		mean = 4
		sd = 4
	return np.random.normal(mean,sd)

def fitFunc1(fit):
	if fit < 30:
		return 0
	elif fit >= 30 and fit < 50:
		return 1
	elif fit >= 50 and fit < 90:
		return 2
	elif fit >= 90:
		return 3

def fitFunc2(fit,pop):
	mean = np.mean(pop)
	sd = np.std(pop) + 0.0001

	z = (fit - mean)/sd

	if z >= -1 and z < 1:
		return 1
	elif z >= 1 and z < 2:
		return 2
	elif z >= 2:
		return 3
	else:
		return 0

def fitFunc3(fit,pop):
	base = 0.3
	highChance = 0.5
	mod = len(pop)*2
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


def makeOff(fit,fitArray,pop):

	#offspring = fitFunc1(fit)
	#offspring = fitFunc2(fit,pop)
	offspring = fitFunc3(fit,pop)

	for x in range(0,offspring):
		if random.random() < catMute:
			mean = 4
			sd = 4
		else:
			mean = fit
			sd = 5
		fitArray.append(np.random.normal(mean,sd))

	return fitArray

def runPop(runs,startSize):
	popArray = []
	countArray = []

	for x in range(0,startSize):
		popArray.append(genBimodal())

	for x in range(0,runs):
		newPop = []
		for i in range(0,len(popArray)):
			newPop = makeOff(popArray[i],newPop,popArray)
		popArray = list(newPop)
		if(random.random() < 1):
		 	popArray.append(genBimodal())
		countArray.append(len(popArray))

	return countArray
	

catMute = 0.1
highPer = 0.4

allPops = []

gens = 10
startPop = 50

for x in range(0,25):
	print x
	allPops.append(runPop(gens,startPop))

countArray = np.arange(gens)

lines = []
sumArray = []

for i in range(0,len(allPops)):
	sumArray.append(allPops[i][-1])
	lines.append(go.Scatter(
					y = allPops[i],
					x = countArray,
					mode = 'lines',
					name = 'Robot ' + str(i),
					line = dict(
		        		color = hex(random.randint(0, 16777215))[2:].upper(),
		        		width = 4)))

plotly.offline.plot({"data":lines}, filename ='Pop.html')

#0, <5, <10, <20, <50, >50, 1
countTable = np.zeros(7)

for s in sumArray:
	if s == 0:
		countTable[0] = countTable[0] + 1
	if s == 1:
		countTable[1] = countTable[1] + 1
	elif s < 5:
		countTable[2] = countTable[2] + 1
	elif s < 10:
		countTable[3] = countTable[3] + 1
	elif s < 20:
		countTable[4] = countTable[4] + 1
	elif s < 50:
		countTable[5] = countTable[5] + 1
	else:
		countTable[6] = countTable[6] + 1


labels = ["0","1","< 5", "< 10", "< 20", "< 50", "> 50"]
values = countTable
colors = ['#ff0400', '#ff9d00', '#fff600','#94ff00', '#00ffdd', "#aa00ff","#ff00e1"]
trace = go.Pie(labels=labels, values=values,
				marker=dict(colors=colors, 
                           line=dict(color='#000000', width=2)))
#plotly.offline.plot([trace], filename='pie.html')



data = [go.Histogram(x = sumArray,
						marker=dict(
					        color='#0000FF'))]

#plotly.offline.plot(data, filename = 'histPop.html')


