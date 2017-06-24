"""
Name: minds.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains creatures' neural networks
"""

from keras.models import Sequential
from keras.layers import Activation
import random
import numpy as np
from bitstring import BitArray

class Mind():
	def __init__(self, numTiles=25, neuronsPerLayer=50, numLayers=2, firstGeneration, DNA):
		self.inputCount = numTiles
		self.outputNeurons = 5 #up, down, left, right, speed

		if firstGeneration:
			#Generate random DNA for the first generation
			self.DNAlength = (inputCount * neuronsPerLayer + neuronsPerLayer * (numLayers - 1) + 
				neuronsPerLayer * outputNeurons + outputNeurons)
			self.DNAbin = []
			for i in range(0, self.DNAlength * 32):
				self.DNAbin.append(random.randint(0,1))
			self.b = BitArray(float=0.00, length=32)
			self.DNAbin = ''.join(self.DNAbin)

			self.DNA = []
			for i in range(0, len(self.DNAbin), 32):
				self.b.bin = self.DNAbin[i:i+32]
				self.DNA.append(b.float)

		#Convert DNA to weights/biases
		weights = []
		count = 0
		l = np.array(self.DNA[count:count + numTiles*neuronsPerLayer])
		count += numTiles*neuronsPerLayer
		l = l.reshape(inputCount, neuronsPerLayer)
		weights.append(l)
		for i in range(numLayers - 1):
			l = np.array(self.DNA[count:count + neuronsPerLayer])
			count += neuronsPerLayer
			weights.append(l)
		l = np.array(self.DNA[count:count + outputNeurons*neuronsPerLayer])
		l = l.reshape(neuronsPerLayer, outputNeurons)
		weights.append(l)
		count += neuronsPerLayer * outputNeurons
		l = np.array(self.DNA[count:count + outputNeurons])
		weights.append(l)

		#Define Keras model of the brain, using sequential layers of activation neurons
		model = Sequential()
		model.add(Dense(neuronsPerLayer, input_shape = (inputCount,), activation='relu'))
		for i in range(numLayers - 1):
			model.add(Activation('relu'))
		model.add(Dense(outputNeurons, activation='relu'))
		model.set_weights(weights)

def think(mind, vision):
	#Use the creatures Keras model and vision to determine direction/speed
	actions = mind.predict(vision)
	return actions