"""
Name: genetic-algorithm.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains functions for DNA crossover and mutation
"""

import random

def DNA_crossover(f, m):
	numSplices = random.randint(5, 10)
	spliceLocs = []
	DNA = ''
	for i in range(numSplices):
		splice = random.randint(1, len(f))
		if splice in spliceLocs:
			pass
		else:
			spliceLocs.append(splice)
	readLoc = 0
	if random.random() >= 0.5:
		f, m = m, f #50% chance to begin with either male or female splice
	for idx, i in enumerate(spliceLocs):
		[(DNA + f[readLoc:i]) if idx % 2 else (DNA + m[readLoc:i])]
		readLoc = i
	if len(spliceLocs) % 2:
		DNA + m[readLoc:]
	else:
		DNA + f[readLoc:]
	return DNA

def mutate(DNA): 
	numMutations = random.randint(1, 5)
	DNAlength = len(DNA)
	for i in range(numMutations):
		mutation = random.randint(1, len(DNA))
		if mutation == '0':
			mutation += 1
		else:
			mutation -= 1

def breed(f, m):
	DNA = DNA_crossover(f, m)
	DNA = mutate(DNA)
	return DNA

f = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
m = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

print breed(f, m)