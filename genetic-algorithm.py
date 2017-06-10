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
	DNA_list = []
	for idx, i in enumerate(spliceLocs):
		[DNA_list.append(f[readLoc:i]) if idx % 2 else DNA_list.append(m[readLoc:i])]
		readLoc = i
	if len(spliceLocs) % 2:
		DNA_list.append(m[readLoc:])
		DNA = ''.join(DNA_list)
	else:
		DNA_list.append(f[readLoc:])
		DNA = ''.join(DNA_list)
	return DNA

def mutate(DNA):
	DNA = list(DNA)
	numMutations = random.randint(1, 5)
	for i in range(numMutations):
		mutation = random.randint(0, (len(DNA) - 1))
		if DNA[mutation] == '0':
			DNA[mutation] = '1'
		else:
			DNA[mutation] = '0'
	DNA = ''.join(DNA)
	return DNA

def breed(f, m):
	DNA = DNA_crossover(f, m)
	DNA = mutate(DNA)
	return DNA

f = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
m = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

dna = breed(f, m)
print dna
print len(dna)