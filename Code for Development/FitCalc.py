
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import random

roboFitness = []
roboAreas = []
fitTime = []
countThat = []
allTime = []

def processString():
	dataArray = []
	copyArray = np.zeros(17)
	lineCount = 0
	lastTime = 0
	time = []

	#filename = 'ConsTests/Robot/DATALOGC-EAST-7-17.txt'
	#filename = "DataLogs/FullDatalogT1-10-7-12.txt"
	#filename = 'DataLogs/DATALOG_RANDOM7-11.txt'
	#filename = 'DataLogs/DATALOG_SIMPLEXOR.txt'
	#filename = 'DataLogs/DATALOG_BIGXOR7-7.txt'
	#filename = "DATALOGSPOTB-719.txt"
	#filename = "XOR727.txt"
	#filename = "LIGHTLOGROBB-POSA.TXT"
	#filename = "010002D1.txt"
	filename = "B2N.TXT"

	w = open(filename,"a")
	w.write("\n end robot test")
	w.close()

	f = open(filename)
	#f = open('DATALOG_RANDOM7-11.txt')
	#f = open('DATALOG_LIGHTSEEKING7-7.txt')
	#f = open('DATALOG_SIMPLEXOR.txt')
	#f = open('Datalogs/FullDatalogT1-10RAND.txt')
	#f = open('DATALOGB-EAST-7-18.txt')
	#f = open('DATALOGEASTC17-17.txt')
	first = True

	for line in f:
		if "robot" in line and not first:
			if int(lastTime) > 4*60*1000:
				allTime.append(time)
				calcFit(dataArray,lineCount)
				lastTime = 0
			dataArray = []
			time = []
			lineCount = 0
		elif "robot" in line:
			first = False
		elif len(line) > 50:
			text = line.split(',')
			if int(text[16]) < (5000 + 20*60*1000) and int(text[16]) > (5000 + 60*1000):
				lastTime = text[16]
				lineCount = lineCount + 1
				time.append(text[16])
				for x in range(0,17):
					copyArray[x] = float(text[x])
				dataArray.append(copyArray)
				copyArray = np.zeros(17)


def xorFit(irVal, photoVal, aCount):
	#IR was 90, photo was 200
	irThres = 49
	photoThres = 126

	isIRAbove = irVal > irThres
	isPhotoAbove = photoVal > photoThres

	if isIRAbove and isPhotoAbove:
		aCount[0] = aCount[0] + 1
		return [0,aCount]
	elif not isIRAbove and not isPhotoAbove:
		aCount[3] = aCount[3] + 1
		return [0,aCount]
	elif not isIRAbove and isPhotoAbove:
		aCount[2] = aCount[2] + 1
		return [1,aCount]
	elif isIRAbove and not isPhotoAbove:
		aCount[1] = aCount[1] + 1
		return [1,aCount]


def calcFit(dArray,lineCount):
	fitness = 0
	count = 0
	fitTrack = []
	countTrack = []
	multipTrack = []

	areaCount = [0,0,0,0]

	for data in dArray:
		irMean = np.mean(data[0:16:2])
		photoMean = np.mean(data[1:17:2])

		XOR = xorFit(irMean,photoMean,areaCount)

		fitness = fitness + XOR[0]
		count = count + 1

		prop1 = (areaCount[1]/float(lineCount))*100.0
		prop2 = (areaCount[2]/float(lineCount))*100.0

		multipFit = prop1 + prop2 + (prop1 * prop2)/10

		multipTrack.append(multipFit)
		countTrack.append(count)
		fitTrack.append(fitness)
		areaCount = XOR[1]


	pFit = multipTrack[-1]#np.round(np.array(fitness)/float(1),4)
	pArea = np.round(np.array(areaCount)/float(lineCount),4)
	pTrack = multipTrack#np.round(np.array(multipTrack)/float(1),4)

	countThat.append(countTrack)
	fitTime.append(pTrack)
	roboFitness.append(pFit)
	roboAreas.append(list(pArea))


processString()

bars = []
lines = []

colors = [['#8db2ef', '#0061ff', '#0061ff','#8db2ef'],
		  ['#ffa8a8', '#ff0000', '#ff0000','#ffa8a8'],
		  ['#aaf4a8', '#18e514', '#18e514','#aaf4a8'],
		  ['#f8f99a', '#f5f900', '#f5f900','#f8f99a'],
		  ['#f9d199', '#ff9400', '#ff9400','#f9d199'],
		  ['#adfff5', '#00ffe1', '#00ffe1','#adfff5'],
		  ['#f99ae2', '#ff00bf', '#ff00bf','#f99ae2'],
		  ['#df96ff', '#b200ff', '#b200ff','#df96ff'],
		  ['#ccc1c1', '#000000', '#000000','#ccc1c1'],
		  ['#629b60', '#088403', '#088403','#629b60'],
		  ['#8db2ef', '#0061ff', '#0061ff','#8db2ef']]


for i in range(0,len(roboFitness)):
	bars.append(go.Bar(
					x = ["+IR +P", "+IR -P", "-IR +P", "-IR -P"],
					y = roboAreas[i],
					name = "Robot " + str(i),
					marker = dict(
		        		color = colors[i])))
	lines.append(go.Scatter(
					y = fitTime[i],
					x = allTime[i],
					mode = 'lines',
					name = 'Robot ' + str(i),
					line = dict(
		        		color = colors[i][1],
		        		width = 4)))

data = bars
layout = go.Layout(
    barmode='group'
)

plotly.offline.plot({"data":data, "layout":layout}, filename ='barPlot.html')

lineData = lines

plotly.offline.plot({"data":lineData}, filename ='linePlot.html')

print "\n \n"

print "Fitness per Robot: " + str(roboFitness) + "\n"
print "Time in each Area per Robot: " + str(roboAreas) + "\n"
print "Areas are: [High IR & Hight Photo, High IR & Low Photo, Low IR & High Photo, Low IR & Low Photo] \n"

print "Mean " + str(np.mean(roboFitness))
print "SD: " + str(np.std(roboFitness))

	