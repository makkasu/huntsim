"""
Name: minds.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains creatures' neural networks
"""

from keras.models import Sequential
from keras.layers import Dense
import random
import numpy as np
import math
from bitstring import BitArray

inputCount = 6
neuronsPerLayer = 15
numHiddenLayers = 1
outputNeurons = 4

model = Sequential()
model.add(Dense(neuronsPerLayer, input_shape = (inputCount,), activation='relu'))
for i in range(numHiddenLayers):
	model.add(Dense(neuronsPerLayer, activation='relu'))
model.add(Dense(outputNeurons, activation='relu'))

def get_weights(firstGeneration=False, DNA=''):
		if firstGeneration:
			#Generate random DNA for the first generation
			DNAlength = (inputCount * neuronsPerLayer + neuronsPerLayer +
				((neuronsPerLayer * neuronsPerLayer) * numHiddenLayers) + neuronsPerLayer * 
				outputNeurons + neuronsPerLayer * numHiddenLayers + outputNeurons)
			DNAbin = []
			for i in range(0, DNAlength * 12):
				DNAbin.append(str(random.randint(0,1)))
			
			DNAbin = ''.join(DNAbin)
			b = BitArray(int=0, length=12)
			DNA = []
			for i in range(0, len(DNAbin), 12):
				b.bin = DNAbin[i:i+12]
				DNA.append(float(b.int))
		else:
			DNAbin = DNA
			DNA = []
			b = BitArray(int=0, length=12)
			for i in range(0, len(DNAbin), 12):
				b.bin = DNAbin[i:i+12]
				DNA.append(float(b.int))

		#Convert DNA to list of weights
		weights = []
		count = 0
		#Normalise our converted DNA to floats between -0.5 and 0.5
		DNA = 2*(DNA-np.float32(-2048))/(np.float32(2047)-np.float32(-2048)) - 1

		#Convert list of weights into shaped arrays for each layer
		#Input weights: inputCount x neuronsPerLayer matrix
		l = np.array(DNA[count:count + inputCount*neuronsPerLayer])
		count += inputCount*neuronsPerLayer
		l = l.reshape(inputCount, neuronsPerLayer)
		weights.append(l)
		#Input activation weights: neuronsPerLayer array
		l = np.array(DNA[count:count + neuronsPerLayer])
		count += neuronsPerLayer
		l = l.reshape(neuronsPerLayer)
		weights.append(l)

		for i in range(numHiddenLayers):
			#Hidden layer weights: neuronsPerLayer x neuronsPerLayer matrix
			l = np.array(DNA[count:count + neuronsPerLayer*neuronsPerLayer])
			count += neuronsPerLayer*neuronsPerLayer
			l = l.reshape(neuronsPerLayer, neuronsPerLayer)
			weights.append(l)
			#Hidden activation weights: neuronsPerLayer array
			l = np.array(DNA[count:count + neuronsPerLayer])
			count += neuronsPerLayer
			l = l.reshape(neuronsPerLayer)
			weights.append(l)
		
		#Output layer weights: neuronsPerLayer x outputNeruons matrix
		l = np.array(DNA[count:count + outputNeurons*neuronsPerLayer])
		l = l.reshape(neuronsPerLayer, outputNeurons)
		weights.append(l)
		count += neuronsPerLayer * outputNeurons
		#Hidden activation weights: neuronsPerLayer array
		l = np.array(DNA[count:count + neuronsPerLayer])
		count += neuronsPerLayer
		l = l.reshape(outputNeurons)
		weights.append(l)
		return weights, DNAbin

def think(weights, vision):
	#Use the creatures Keras model and vision to determine direction/speed
	impulse = np.float32(2*random.random() - 1)
	tempList = []
	tempList.append(impulse)
	# vision = np.array([tempList])
	vision.append(impulse)
	# print vision
	vision2 = np.array([vision]) #Flatten array
	# print vision2
	# print "\n\n"
	model.set_weights(weights)
	actions = model.predict(vision2)
	return actions