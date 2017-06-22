"""
Name: mapfuncs.py 
Author: Max Potter
Date: June 2017
Description:
	- Contains functions relating to the map
	- create_map generates a 'Voronoi' map of terrain for use in huntsim.py
"""

from random import randint, choice

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
	    typeList = [0] * 4 + [1] * 2 + [2] * 1 # weighted list of types
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
