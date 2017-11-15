f = open('datalog.txt')

d = open('rData.txt',"w")
roboCount = 0

d.write("IR0,P0,IR1,P1,IR2,P2,IR3,P3,IR4,P4,IR5,P5,IR6,P6,IR7,P7,Time,RoboNum \n")

for line in f:
	if "robot" in line:
		roboCount = roboCount+1
	else:
		d.write(line[:-2]+str(roboCount)+ "\n")

f.close()
d.close()

