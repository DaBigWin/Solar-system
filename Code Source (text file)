#To Do/Done:
	#Find how much the direction should change given a veloctiy and centripetal accel. |done see 

#Limitations:
	#The solar system is not 2D. However, it is somewhat algined on a plane so not too off
	#Also, orbits are not circular, but this simulation assumes they are. Their elipcises are nearly perfect circles anyway (ex. earth and jupiter)
	#Assuming the sun is moving?
	#Assuming sun is the only gravitater?

#Bugs:
	#Not working? Spirals instead of circling. Suggessted 1 (more presice) or 10 day cycle to see effects quickly
		#Solution 1: Move it 1 move, plot, then move it back. Then move it 2 move, plot, then move it back. Then move it 3 move, plot, then move it back... | Done. Did not work

#Imports
import matplotlib.pyplot as plt
import math as mt
import time
import numpy as np
import random as rm

plt.clf()

#Calculates the acceleration due to gravity given a mass of gravitater and distance between two objects using the equation for gravity accel, g*m/r**2
def gravityaccel(m, r):
	G = 6.67* 10**-11
	accel = (G)*(m)/(r)**2
	return accel
	
#Calculates distance between two objects given coordinates as lists
def distance(object1, object2):
	xDISTANCE = abs(object1[0] - object2[0])
	yDISTANCE = abs(object1[1] - object2[1])
	DISTANCE = mt.sqrt( xDISTANCE**2 + yDISTANCE**2 )
	return DISTANCE

#Changes seconds to years
def daysSeconds(days):
	Years = days * 60 * 60 * 24
	return Years

#Calculates the change in x and y coor. based off velocity and direction. 
def directMovement(direction, velocity):
	if direction == 360:
		changeX = 0
		changeY = velocity
		
	elif direction < 360:
		directionPerc = 360-direction
		changeX = -1 * velocity * (directionPerc/90)
		changeY = velocity * ( (90-directionPerc) /90)
		
		if direction < 270:
			directionPerc = 270-direction
			changeX = -1 * velocity * ( (90-directionPerc) /90)
			changeY = -1 * velocity * (directionPerc/90)
			
			if direction < 180:
				directionPerc = 180-direction
				changeX = velocity * (directionPerc/90)
				changeY = -1 * velocity * ( (90-directionPerc) /90)
		
				if direction < 90:
					directionPerc = 90-direction
					changeX = velocity * ( (90-directionPerc) /90)
					changeY = velocity * (directionPerc/90)
	
	#print(direction)
	#print(velocity)
	#print(changeX, changeY)
	#print()
	return [changeX, changeY]
					
#Finds directity (change in direction per sec). Does so by calculating the time it takes for a quater orbit (90 degree change) and then making that into a per sec. Assumes circular orbits.
def directChange(radius, velocity):
	circumfrance = 2*radius*mt.pi
	QuarterPeriod = (circumfrance/4) / velocity
	directity = 90/QuarterPeriod
	return directity

#Asks for how long a cycle of movement should take
cycleTime = float(input("How long to complete a cycle? (in days)"))
cycleTime = daysSeconds(cycleTime)

#Counts seconds
secondCounter = 0	
					
#Some values (givens) in kg 
radiusEarth = 6370000
radiusMars = 3389500
radiusSun = 695700100

massEarth = 5.98* 10**24
massMars = 6.39* 10**23
massSun = 1.98* 10**30

#Sets originating coordinates and info [x (0), y (1), direction (2), color (3), plotsize (4), radius (5), mass (6), velocity (7)]
CoorEarth = [1.5* 10**11, 0, 360, "g", 50, radiusEarth, massEarth, "N/A"]
CoorMars = [2.4296* 10**11, 0, 360, "r", 40, radiusMars, massMars, "N/A"]
CoorSun = [0, 0, 360, "y", 100, radiusSun, massSun, 0]
Coors = [CoorEarth,CoorMars,CoorSun]

#Game loop starts
while 1 == 1:
	#Distances from planets to other bodies
	distance(CoorEarth,CoorSun)
	distance(CoorMars,CoorSun)
	
	#Accelerations due to gravities of other masses
	gravityaccel(massSun, distance(CoorEarth,CoorSun))
	
	#Continues time
	secondCounter += 1
	
	#velocties are m per second. Found with equation sqrt(gravityaccel * radius/mass) by manipulating the equation for centripetal accel (Ca = v^2/r) -> (sqrt(Ca * r) = v). In this case, ac is gravityaccel. If it is the sun (color "y"), set velocity to 0 automaticly to avoid a division by 0
	for planet in Coors:
		if planet[3] == 'y':
			planet[7] = 0
		else:
			planet[7] = secondCounter * mt.sqrt(gravityaccel(massSun, distance(planet,CoorSun)) * distance(planet,CoorSun))
	
	#Changes direction of the planets in their centripetal paths/orbits. Only for the gravity of the sun. If it is the sun (color "y"), don't change direction to avoid a division by 0
	for planet in Coors:
		if planet[3] == 'y':
			break
		else:
			#Repeats direction change secondCounter times
			directityPlanet = directChange(distance(planet,CoorSun), planet[7]/secondCounter)
			if planet[3] == 'g':
					directityEarth = directityPlanet
			
			planet[2] -= directityPlanet * secondCounter
			#For all the 360's in a direction, remove them
			planet[2] -= mt.floor(planet[2]/360)*360
			
			#Counter = 0
			#while not Counter == secondCounter:
				#planet[2] -= directityPlanet
	
				##if a direction is less than/equal to 0, add 360
				#for Coor in Coors:
					#if Coor[2] <= 0:
						#Coor[2] += 360
				
				#Counter += 1
	
	#Coordinates and movements. See direct movement()
	for Coor in Coors:
		changeXY = directMovement( Coor[2], Coor[7] )
		Coor[0] += changeXY[0]
		Coor[1] += changeXY[1]
	
	#Prints days passed
	if secondCounter % daysSeconds(1) == 0:
		print(secondCounter/86400)
	
	#Plots every cycle
	if secondCounter % cycleTime == 0:
		##Bug fix
		#plt.clf()
	
		#Plots planets/sun/object	
		for Coor in Coors:
		
			#Plots orbit paths
			orbit = plt.Circle((0, 0), distance(Coor, CoorSun), fill=False)
			plt.gca().add_patch(orbit)
			
			#Plots all bodies
			plt.scatter(Coor[0], Coor[1], color = Coor[3], s = Coor[4])
			
		#Format	
		plt.xticks( np.arange(-2.5 * 10**11, 4.1 * 10**11, 0.5 * 10**11))
		plt.yticks( np.arange(-2.5 * 10**11, 2.51 * 10**11, 0.5 * 10**11))
		
		#Bug fix
		#Shows the ideal orbit of a circle, mars and earth
		orbit = plt.Circle((0, 0), 1.5* 10**11, color='r', fill=False)
		plt.gca().add_patch(orbit)
		
		orbit = plt.Circle((0, 0), 2.4296* 10**11, color='r', fill=False)
		plt.gca().add_patch(orbit)
		
		#time.sleep(0.5)
		plt.show()
		
		##Bug fix
		#Displays some variables relating to the 
		print("Change in direction of earth" + str(directityEarth))
		print("Distance from earth to sun" + str(distance(CoorEarth, CoorSun)))
		print("Velocity of the earth" + str(CoorEarth[7]/secondCounter))
		
		
	#Resets movement
	CoorEarth = [1.5* 10**11, 0, 360, "g", 50, radiusEarth, massEarth, "N/A"]
	CoorMars = [2.4296* 10**11, 0, 360, "r", 40, radiusMars, massMars, "N/A"]
	CoorSun = [0, 0, 360, "y", 100, radiusSun, massSun, 0]
	Coors = [CoorEarth,CoorMars,CoorSun]
