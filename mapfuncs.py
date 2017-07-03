"""
Name: mapfuncs.py 
Author: Max Potter
Date: June 2017
Description:
	- Contains functions relating to the map
	- create_map generates a 'Voronoi' map of terrain for use in huntsim.py
"""

from random import randint, choice
from settings import *

def create_map(width, height, minSeeds, maxSeeds):
	"""
	Create a number of 'seeds' from which patches of terrain will be built.
	Each seed has a random type: dirt, grass or wood. 
	Each tile checks to see which seed it is nearest too and gains that type.
	"""
	seedNumber = randint(minSeeds,maxSeeds) # the number of seeds 
	#Generate list of seeds
	seedList = []
	for i in range(seedNumber):
	    point = (randint(0,height),randint(0,width))
	    typeList = [dirt] * 4 + [grass] * 2 + [wood] * 1 # weighted list of types
	    seedType = choice(typeList)
	    seedList.append((point,seedType)) # add a seed at a random point with a random type to the list
	#For all tiles, which seed type is closest? Adopt that type.
	tilemap = [[None for column in range(width)] for row in range(height)] # create blank tilemap
	for row in range(height):
	    for column in range(width):
	        # check distance to all seeds, which is closest
	        distances = []
	        for seed in seedList:
	            dy = abs(seed[0][0] - row)
	            dx = abs(seed[0][1] - column)
	            d = (dx**2 + dy**2)**(0.5)
	            distances.append((d,i))
	        # find the index of the minimum distance (same as corresponding seed index)
	        index_min = min(xrange(len(distances)), key=distances.__getitem__)
	        closestSeed = seedList[index_min]
	        tilemap[row][column] = closestSeed[1]

	return tilemap

def find_tile(creature, tileSize, height, width):
	"""
	Takes a creature and finds the tilemap indicies of the tile it is standing on.
	Forces indicies to be within the bounds of tilemap.
	"""
	j = int(creature.rect.centerx/tileSize)
	i = int(creature.rect.centery/tileSize)

	if i < 0:
		i = 0
	if i >= height:
		i = height - 1
	if j < 0:
		j = 0
	if j >= width:
		j = width - 1
		
	return i, j

def get_vision(i, j, tilemap, height, width):
	"""
	Takes tilemap and indicies, returns 5x5 section of tilemap centred on (i,j).
	"""
	#Set up 5x5 array, every element is -1 (which will indicate 'seeing off map')
	vision = [[wall for column in range(5)] for row in range(5)]

	for idx in range(5):
		for jdx in range(5):
			#Find tilemap index we want to look at
			tmidx = i - 2 + idx
			tmjdx = j - 2 + jdx

			#Skip changing vision list if index is out of tilemap bounds
			if tmidx < 0 or tmjdx < 0 or tmidx > height - 1 or tmjdx < 0 or tmjdx > width - 1:
				continue

			vision[idx][jdx] = tilemap[i - 2 + idx][j - 2 + jdx]

	# ********* THIS VISION CODE IS ONLY FOR TIGERS - WHEN DEER START MOVING, REWORK!
	up = [vision[1][0],vision[2][0],vision[3][0],vision[1][1],vision[2][1],vision[3][1]]
	down = [vision[1][3],vision[2][3],vision[3][3],vision[1][4],vision[2][4],vision[3][4]]
	left = [vision[0][1],vision[0][2],vision[0][3],vision[1][1],vision[1][2],vision[1][3]]
	right = [vision[3][1],vision[3][2],vision[3][3],vision[4][1],vision[4][2],vision[4][3]]
	centre = vision[2][2]

	directions = [up,down,left,right]
	vision2 = []
	for direction in directions:
		if deerColour in direction:
			vision2.append(deerColour)
		elif wall in direction:
			vision2.append(wall)
		else:
			vision2.append(max(set(direction), key=direction.count))
	vision2.append(centre)

	return vision2
