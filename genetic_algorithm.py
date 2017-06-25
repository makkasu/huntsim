"""
Name: genetic_algorithm.py
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains functions for DNA crossover and mutation
"""

import random

#Lists of children waiting to be born
tPregnancies = []
dPregnancies = []

#Lists of most fit parents
tGenepool = []
dGenepool = []

#List for selecting index when choosing parents
idxList = ([0] * 15 + [1] * 14 + [2] * 13 + [3] * 12 + [4] * 11 +
			[5] * 10 + [6] * 9 + [7] * 8 + [8] * 7 + [9] * 6 + 
			[10] * 5 + [11] * 4 + [12] * 3 + [13] * 2 + [14] * 1)

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
	spliceLocs.sort()
	readLoc = 0
	if random.random() >= 0.5:
		f, m = m, f #50% chance to begin with either male or female splice
	DNA_c1 = []
	DNA_c2 = []
	for idx, i in enumerate(spliceLocs):
		[DNA_c1.append(f[readLoc:i]) if idx % 2 else DNA_c1.append(m[readLoc:i])]
		[DNA_c2.append(m[readLoc:i]) if idx % 2 else DNA_c2.append(f[readLoc:i])]
		readLoc = i
	if len(spliceLocs) % 2:
		DNA_c1.append(m[readLoc:])
		DNA_c2.append(f[readLoc:])
		DNA1 = ''.join(DNA_c1)
		DNA2 = ''.join(DNA_c2)
	else:
		DNA_c1.append(f[readLoc:])
		DNA_c2.append(m[readLoc:])
		DNA1 = ''.join(DNA_c1)
		DNA2 = ''.join(DNA_c2)
	return DNA1, DNA2

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

def breed(ctype):
	#Select parents, with preference given to higher fitness scores
	idx = random.choice(idxList)
	idx2 = idx
	while idx2 == idx:
		idx2 = random.choice(idxList)
	
	if ctype == "tiger":
		#Take the DNA component from our random index values
		DNA1, DNA2 = DNA_crossover(tGenepool[idx][1], tGenepool[idx2][1])
		DNA1 = mutate(DNA1)
		DNA2 = mutate(DNA2)
		tPregnancies.append(DNA1)
		tPregnancies.append(DNA2)

	elif ctype == "deer":
		#Take the DNA component from our random index values
		DNA1, DNA2 = DNA_crossover(dGenepool[idx][1], dGenepool[idx2][1])
		DNA1 = mutate(DNA1)
		DNA2 = mutate(DNA2)
		dPregnancies.append(DNA1)
		dPregnancies.append(DNA2)

def get_DNA(ctype):
	DNA = ''
	if ctype == "tiger":
		DNA = tPregnancies[0]
		del tPregnancies[0]
	elif ctype == "deer":
		DNA = dPregnancies[0]
		del dPregnancies[0]
	return DNA

def pool(fitness, DNA, ctype):
	"""
	Check if our candidate has a good enough fitness score to be a
	candidate parent. If so, add it to the list and if necessary sort
	and trim the list to keep it at the appropriate size.
	"""
	print 'Deer gene pool/pregnancies'
	print len(dGenepool)
	print len(dPregnancies)
	print 'Tiger gene pool/pregnancies'
	print len(tGenepool)
	print len(tPregnancies)

	if ctype == "deer" and len(dGenepool) < 15:
		dGenepool.append([fitness, DNA])
		dGenepool.sort(key=lambda x: x[0], reverse=True)
	elif ctype == "deer" and len(dGenepool) >= 15:
		if fitness > dGenepool[14][0]:
			dGenepool.append([fitness, DNA])
			dGenepool.sort(key=lambda x: x[0], reverse=True)
			del dGenepool[15:]

	elif ctype == "tiger" and len (tGenepool) < 15:
		tGenepool.append([fitness, DNA])
		tGenepool.sort(key=lambda x: x[0], reverse=True)
	elif ctype == "tiger" and len(tGenepool) >= 15:
		if fitness > tGenepool[14][0]:
			tGenepool.append([fitness, DNA])
			tGenepool.sort(key=lambda x: x[0], reverse=True)
			del tGenepool[15:]


#Add genepools for deer and tiger. 
#Add a pool function which is called from huntim->creature and passes DNA, fitness and ctype
#Add a select function which chooses two parents from genepool, weighted to select the top ones

# f = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
# m = '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'

# dna1, dna2 = breed(f, m)
# print dna1, '\n', dna2
# print len(dna1)
# print dna1.count('1') 
# print dna2.count('1')

#Add parent_select function, and lists for deer/tigers which keep the top 15 or so DNA sequences.
#parent_select chooses the two strings to mix
#Each breed should produce 2 children (inverse of each other prior to mutation) so that all DNA is represented. 