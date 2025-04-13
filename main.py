#To Do/Done:
	#Find how much the direction should change given a veloctiy and centripetal accel. |done see
	#Add all the other planets: Sun (d), Mercury (d), Venus (d), Earth (d), Mars (d), Jupiter (d), Saturn (d), Uranus (d), Neptune (d)
		#Put the planets in their currentday states | For future scientists
	#Add the meteor code. |done see velocitation and totals	
		#Calculate the radius given a mass (and a constant density) | HOOOOOOOOW? you know what not important
	#Add in the collision code |For future scientists
		#What I can do is simply if the radiusi are touching I just split them apart |
	#Observe Keplers laws | Done!
	#Change the float settings | Reaserch needed! Done!
	#Settle on a time frame |365 days?
		#Also, once done, draw the line of the meteor movement from its start and end(end time) positions so that we can see how far the meteor has progressed and will progress. |done(?)

#Limitations:
	#The solar system is not 2D. However, it is somewhat algined on a plane so not too off
	#Also, orbits are not circular, but this simulation assumes they are. Their elipcises are nearly perfect circles anyway (ex. earth and jupiter)
	#Assuming sun is the only "true" gravitater:
		#For other gravivites (planet to planet, astreiod to planets/sun and viseversa, sun to planets), because they aren't orbiting and I don't know how to change direction given gravity, i simply moved the object gravityaccel m towards the gravitater{}
	#No collision data

#Bugs:
	#Not working? Spirals instead of circling. Suggessted 1 (more presice) or 10 day cycle to see effects quickly
		#Solution 1: Move it 1 move, plot, then move it back. Then move it 2 move, plot, then move it back. Then move it 3 move, plot, then move it back... | Done. Did not work
		#Solution 2: Sin and cos. 
		#is it too accurate?
		#FIXED!!!!!!!!!!!!
	#The move_towards was causing some sort of issue resulting in planets going straight to each other's positions
		#Fixed,the function was adding to Coor2 when it should have been adding to Coor1

#Imports
import matplotlib.pyplot as plt
import math as mt
import time
import numpy as np
import random as rm
from decimal import Decimal, getcontext

#Sets deciaml places to blank
getcontext().prec = 50

plt.clf()

#Calculates the acceleration due to gravity given a mass of gravitater and distance between two objects using the equation for gravity accel, g*m/r**2
def gravityaccel(m, r):
	G = Decimal(6.67* 10**-11)
	accel = (G)*(Decimal(m))/(Decimal(r))**Decimal(2)
	return accel
#Calculates the force due to gravity given two masses and distance between two objects using the equation for gravity force, g*m1*m2/r**2
		
#Calculates distance between two objects given coordinates as lists
def distance(object1, object2):
	xDISTANCE = abs(object1[0] - object2[0])
	yDISTANCE = abs(object1[1] - object2[1])
	DISTANCE = Decimal(mt.sqrt( xDISTANCE**2 + yDISTANCE**2 ))
	return Decimal(DISTANCE)

#Copies a list but distingueshes it by adding 'dist' to the end. Only works for once nested lists.
def copyNopullLevel1(copyList):
	returnList = ['placeholder']
	for nestlist in copyList:
		copynest = nestlist.copy()
		copynest.append('dist')
		returnList.append(copynest)
	
	returnList.pop(returnList.index('placeholder'))	
		
	return returnList	

#moves an object1 towards an object2. I used chatgpt for this...
def move_towards(Coor1, Coor2, velocity):
	movedistance = distance(Coor1, Coor2)
	
	if movedistance == 0:
		return Coor1
	
	#Calculates the fraction of the distance to move and caps it at 1 so it doens't go farther
	ratio = min(Decimal(velocity/movedistance), 1)
	
	#Computes new coordiantes
	changeX = Decimal((ratio * (Coor2[0] - Coor1[0]) ))
	changeY = Decimal((ratio * (Coor2[1] - Coor1[1]) ))
	
	return [changeX, changeY]

#Changes seconds to years
def daysSeconds(days):
	Years = days * 60 * 60 * 24
	return Decimal(Years)

#changes curve length to line length
def arcToChord(radius, arcl):
	#arcl = radius * angle, so angle = arcl/radius
	arcangle = arcl/radius
	
	#This formula gives the chord length
	chordl = 2 * radius * mt.sin(arcangle/2)
	
	return chordl

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
	return [Decimal(changeX), Decimal(changeY)]
										
#Finds directity (change in direction per sec). Does so by calculating the time it takes for a quater orbit (90 degree change) and then making that into a per sec. Assumes circular orbits.
def directChange(radius, velocity):
	circumfrance = Decimal(2)*Decimal(radius)*Decimal(mt.pi)
	QuarterPeriod = circumfrance / Decimal(velocity)
	directity = Decimal(360)/QuarterPeriod
	return directity

#Calculate orbit time (t), each second it is seconds/t * 360 gives the degrees (d). Convert degrees to radians. Then use cos and sin to find x and y in the circle respectivly. Coor is [cos(d),sin(d)], each times the radius
def directBySinCos(velocity, radius, timestamp):
	circumfrance = Decimal(2) * radius * Decimal(mt.pi)
	orbitalPeriod = Decimal(circumfrance/velocity)
	
	degrees = Decimal(timestamp/orbitalPeriod) * Decimal(360)
	radians = Decimal(mt.radians(degrees))
	
	coor = [Decimal(mt.cos(radians))*radius,Decimal(mt.sin(radians))*radius]
	return coor
	
#Asks for how long a cycle of movement should take
cycleTime = float(input("How long to complete a cycle? (in days)"))
limit = int(input("End day?"))
cycleTime = daysSeconds(cycleTime)

#Counts seconds
secondCounter = Decimal(0)	
					
#Some example values (givens) in kg and m
radiusEarth = 6370000
radiusMars = 3389500
radiusSun = 695700100

massEarth = 5.98* 10**24
massMars = 6.39* 10**23
massSun = 1.98* 10**30

#Sets originating coordinates and info [x (0), y (1), direction (2), color (3), plotsize (4), radius (5), mass (6), velocity (7)]
CoorSun = [0, 0, 360, "y", 200, radiusSun, massSun, 0]
CoorMercury = [6.75023* 10**10,0, 360, "firebrick", 30, 2440000, 3.285* 10**23, "N/A"]
CoorVenus = [1.080127* 10**11, 0, 360, "coral", 45, 6051777, 4.867* 10**24, "N/A"]
CoorEarth = [1.5* 10**11, 0, 360, "g", 50, radiusEarth, massEarth, "N/A"]
CoorMars = [2.4296* 10**11, 0, 360, "r", 40, radiusMars, massMars, "N/A"]
CoorJupiter = [7.648729* 10**11,0, 360, "goldenrod", 120, 69911512.7, 1.89813* 10**27, "N/A"]
CoorSaturn = [1.435551* 10**12,0, 360, "olive", 110, 58232000, 5.683* 10**26, "N/A"]
CoorUranus = [2.921442* 10**12,0, 360, "turquoise", 80, 25361652, 8.681* 10**25, "N/A"]
CoorNeptune = [4.4710795* 10**12,0, 360, "mediumslateblue", 70, 24621353, 1.024* 10**26, 'N/A']

AstrList = input("For asteriod: Starting position (X and Y), Direction(°), Mass(kg), Velocity(m/s). Seperate with commas: ")
AstrList = AstrList.split(',')
#AstrRad = mt.sqrt(AstrList[3]/3.5)
AstrRad = 100000
CoorAstreiod = [int(AstrList[0]),int(AstrList[1]), int(AstrList[2]), "0.5",10, int(AstrRad),float(AstrList[3]), int(AstrList[4])]

#originalCoors = [CoorSun,CoorEarth, CoorMars]
Coors = [CoorSun, CoorMercury,CoorVenus,CoorEarth,CoorMars,CoorJupiter,CoorSaturn,CoorUranus,CoorNeptune, CoorAstreiod]
#Sets all values to Decimal() except for color (string) and velocity (yet to be a value)
for Coor in Coors:
	for value in Coor:
		
		if not value == Coor[3] and not value == Coor[7]:
			
			Coors[Coors.index(Coor)][Coor.index(value)] = Decimal(value)

#Note: because of the function and as to make the lists not be affected by Coors, each originalCoors[x][-1] is 'dist'. x can be any number withn the range of the list.
originalCoors = copyNopullLevel1(Coors)
#Removes astreiod from original Coors list
for originalCoor in originalCoors:
	if originalCoor[3] == '0.5':
		originalCoors.pop(originalCoors.index(originalCoor))

#list of disorted distances.
distancesdistort = []
for x in originalCoors:
    distancesdistort.append([0])
#list of percent changes.
distancepercentchanges = []
for x in originalCoors:
    distancepercentchanges.append([0])

#Game loop starts
while secondCounter/86400 < limit:
    #Distances from planets to other bodies
	distance(CoorEarth,Coors[0])
	distance(CoorMars,Coors[0])
	
	#Accelerations due to gravities of other masses
	gravityaccel(massSun, distance(CoorEarth,Coors[0]))
	
	#Continues time
	secondCounter += 1

	#velocties are m per second. Found with equation sqrt(gravityaccel * radius/mass) by manipulating the equation for centripetal accel (Ca = v^2/r) -> (sqrt(Ca * r) = v). In this case, ac is gravityaccel. If it is the sun (color "y"), set velocity to 0 automaticly to avoid a division by 0. If it is the meteor (color '0.5'), skip.
	for planet in Coors:
		if planet[3] == 'y':
			planet[7] = Decimal(0)
		else:
			planet[7] = Decimal(mt.sqrt(gravityaccel(Coors[0][6], distance(planet,Coors[0])) * distance(planet,Coors[0])))
	#Coordinates and movements. See directBySinCos()
	for Coor in Coors:
		if Coor[3] == 'y':
			continue
		elif Coor[3] == '0.5':
			continue
		else: 
			newCoors = directBySinCos(Coor[7],distance(Coor,Coors[0]), secondCounter)
			
		Coor[0] = newCoors[0]
		Coor[1] = newCoors[1]
	
	#does the same thing for original coor as to compare orbits
	for planet in originalCoors:
		if planet[3] == 'y':
			planet[7] = Decimal(0)
		else:
			planet[7] = Decimal(mt.sqrt(gravityaccel(originalCoors[0][6], distance(planet,originalCoors[0])) * distance(planet,originalCoors[0])))
	#Coordinates and movements. See directBySinCos()
	for Coor in originalCoors:
		if Coor[3] == 'y':
			neworiginalCoors = [Decimal(0),Decimal(0)]
		elif Coor[3] == '0.5':
			continue
		else: 
			neworiginalCoors = directBySinCos(Coor[7],distance(Coor,originalCoors[0]), secondCounter)
			
		Coor[0] = neworiginalCoors[0]
		Coor[1] = neworiginalCoors[1]
	
	#Velocitates the meteor (see directmovement; velocity and direction are prior inputs)
	changeXY = directMovement(Coors[-1][2], Coors[-1][7])
	Coors[-1][0] += changeXY[0]
	Coors[-1][1] += changeXY[1]
	
	#Moves planet towards other gravitaters
	newcoord = ['placeholder']
	
	for planet in Coors:
		for centerplanet in Coors:
			#not towards self or sun (again)
			if centerplanet[3] == 'y' or centerplanet == planet:
				continue
				
			#Calculate the gravitational accel between planets
			pullmovement = gravityaccel(centerplanet[6], distance(centerplanet,planet))
			#See function
			newcoord.append(move_towards(planet, centerplanet, pullmovement))
	newcoord.pop(newcoord.index('placeholder'))
	
	#totals the new movements of each planet
	totalsX = ['placeholder']
	totalsY = ['placeholder']
	
	#inserts len(Coors) 0's to jumpstart the process
	for x in Coors:
		totalsX.append(0)
	for x in Coors:
		totalsY.append(0)
	
	totalsX.pop(totalsX.index('placeholder'))
	totalsY.pop(totalsY.index('placeholder'))
	
	for new in newcoord:
		for coor in Coors:
			if newcoord.index(new) == Coors.index(coor):
				totalsX[Coors.index(coor)] += new[0] 
				totalsY[Coors.index(coor)] += new[1]
	#for totalX in totalsX:
		#index = totalsX.index(totalX)
		#totalsX[index] /= Decimal((len(Coors) - 2))
	#for totalY in totalsY:
		#index = totalsY.index(totalY)
		#totalsY[index] /= Decimal((len(Coors) - 2))
	
	#newcoord contains too many variantes. need to find a way to directly give the total coors (which are the new coors) to the coorisponding Coors planets
	for totalX in totalsX:
		index = totalsX.index(totalX)
		
		#replaces coors with totals
		Coors[index][0] += Decimal(totalX)
	for totalY in totalsY:
		index = totalsY.index(totalY)
		
		#replaces coors with totals
		Coors[index][1] += Decimal(totalY) 
		
	#Prints days passed
	if secondCounter % daysSeconds(1) == 0:
		print(secondCounter/86400)
	
	#Plots every cycle
	if secondCounter % cycleTime == 0:
		##Bug fix
		plt.clf()
		
		#Format	
		timerdisplay = "Days: " + str(secondCounter/86400) + " (Seconds: " + str(secondCounter) + ")"
		plt.title(timerdisplay)
		
		innerbodies = ['y','firebrick','coral','g','r','goldenrod']
		outerbodies = ['olive','turquoise','mediumslateblue']
		
		#Plots only sun, mercury, venus, earth, and mars so the plane is not overloaded
		for Coor in Coors:
			
			if Coor[3] in outerbodies:
				continue
			if Coor[3] == '0.5' and distance(Coors[0],Coor) > distance(Coors[0],Coors[5]):
				continue
			
			#Plots orbit paths
			if not Coor[3] == '0.5':
				orbit = plt.Circle((0, 0), distance(Coor, Coors[0]), fill=False)
				plt.gca().add_patch(orbit)
			elif Coor[3] == '0.5':
				portion = daysSeconds(365) - secondCounter
				fowardcoor = directMovement(Coor[2], Coor[7]*Decimal( portion ))
				fc = [Coor[0]+fowardcoor[0], Coor[1]+fowardcoor[1]]
				backwardcoor = directMovement((Coor[2]+180)%360, Coor[7]*Decimal( secondCounter ))
				bc = [Coor[0]+backwardcoor[0], Coor[1]+backwardcoor[1]]
				plt.plot([fc[0],bc[0]],[fc[1],bc[1]], color = '0.5', alpha = 0.1)
			
			#Plots all bodies
			plt.scatter(float(Coor[0]), float(Coor[1]), color = Coor[3], s = float(Coor[4]))
		#Shows the ideal orbit of a circle for planets
		for Coor in originalCoors:
			
			if Coor[3] in outerbodies:
				continue
			if Coor[3] == '0.5' and distance(Coors[0],Coor) > distance(Coors[0],Coors[5]):
				continue
			
			plt.scatter(float(Coor[0]), float(Coor[1]), color = Coor[3], s = float(Coor[4]), alpha = 0.25, edgecolors='red')
			
			orbit = plt.Circle((0, 0), distance([0,0],Coor), color='r', fill=False)
			plt.gca().add_patch(orbit)
		
		#time.sleep(0.5)
		plt.show()
		
		#Plots the rest of planets/objects 	
		for Coor in Coors:
		
			if Coor[3] in innerbodies:
				continue
			if Coor[3] == '0.5' and distance(Coors[0],Coor) < distance(Coors[0],Coors[5]):
				continue		
		
			#Plots orbit paths
			if not Coor[3] == '0.5':
				orbit = plt.Circle((0, 0), distance(Coor, Coors[0]), fill=False)
				plt.gca().add_patch(orbit)
			elif Coor[3] == '0.5':
				portion = daysSeconds(365) - secondCounter
				fowardcoor = directMovement(Coor[2], Coor[7]*Decimal( portion ))
				fc = [Coor[0]+fowardcoor[0], Coor[1]+fowardcoor[1]]
				backwardcoor = directMovement((Coor[2]+180)%360, Coor[7]*Decimal( secondCounter ))
				bc = [Coor[0]+backwardcoor[0], Coor[1]+backwardcoor[1]]
				plt.plot([fc[0],bc[0]],[fc[1],bc[1]], color = '0.5', alpha = 0.1)
			
			#Plots all bodies
			plt.scatter(float(Coor[0]), float(Coor[1]), color = Coor[3], s = float(Coor[4]))	
		#Shows the ideal orbit of a circle for planets
		for Coor in originalCoors:
			
			plt.scatter(float(Coor[0]), float(Coor[1]), color = Coor[3], s = float(Coor[4]), alpha = 0.25, edgecolors='red')
			
			orbit = plt.Circle((0, 0), distance([0,0],Coor), color='r', fill=False)
			plt.gca().add_patch(orbit)
		
		plt.show()
		
		#data about how far orbits are from their intended ones, also some kepler law observance
		for coor in Coors:
			for originalcoor in originalCoors:
				if coor[3] == originalcoor[3]:
					index = originalCoors.index(originalcoor)
                    
					#prints body id (color) and distance from ideal
					print(coor[3])
					print("Distance from ideal position (m): "+ str(distance(coor, originalcoor)))
                    
                    #add the distance to a list of distances
					distancesdistort[index].append(distance(coor, originalcoor))
                    #prints the change in distance if not going from 0 to distance
					if not len(distancesdistort[index]) == 2:
						days = int(secondCounter/Decimal(86400))
						distancepercentchange = Decimal(distancesdistort[index][days] - distancesdistort[index][days-1])
						print("Increase in distance: "+ str(distancepercentchange))
						distancepercentchanges[index].append(distancepercentchange)
                    
                    #prints average change
					print('Average increase: ' +str(Decimal(sum(distancepercentchanges[index])/len(distancepercentchanges[index]))))
					
					#if it is the sun, kepler's laws don't rly apply in this way so continue
					if originalcoor[3] == 'y':
						continue
					
					#print the semi-major axis, area, and t^2/a^3
					print("Ideal orbits:")
					semiaxis = distance(originalCoors[0], originalcoor)
					print('	Semi-major axis (m): '+ str(semiaxis))
					print(' Area made (m^2): '+ str( (Decimal(mt.pi) * semiaxis**2) * (cycleTime/daysSeconds(365)) ))
					circumfrance = Decimal(2)*Decimal(semiaxis)*Decimal(mt.pi)
					orbitalP = Decimal(circumfrance / Decimal(originalcoor[7]))
					print('	T^2/A^3 = ' + str(orbitalP**2/semiaxis**3) )
					
					print()
                             
		print('----------------------------------')
plt.clf()

for planet in distancesdistort:
    planetindex = distancesdistort.index(planet)
    print( Coors[planetindex][3])
    print( planet )
    print( str(Decimal(sum(distancepercentchanges[planetindex])/len(distancepercentchanges[planetindex]))))
    print( )
    
    
for planet in distancesdistort:
    planetindex = distancesdistort.index(planet)
    ##plots distance
    dayplot = 0
    for disttance in planet:
        dayplot += 1
        plt.scatter( dayplot, disttance, color = Coors[index][3])
        ##plots lines inbetween scatters
        if not dayplot == 1:
            plt.plot( [dayplot-1, dayplot], [planet[dayplot-2], disttance], color = Coors[index][3])
    
    ##plots average change as a line
    plt.plot( [1,dayplot], [sum(distancepercentchanges[planetindex])/len(distancepercentchanges[planetindex]),sum(distancepercentchanges[planetindex])/len(distancepercentchanges[planetindex])], color = 'r' )
    
    ##formating
    plt.text( dayplot, disttance, str(disttance))
    plt.title(str(Coors[planetindex][3]))
    plt.show()
