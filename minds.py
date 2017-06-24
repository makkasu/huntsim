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
	def __init__(self, numTiles=25, neuronsPerLayer=50, numLayers=2, firstGeneration=False, DNA=''):
		self.inputCount = numTiles
		self.outputNeurons = 5 #up, down, left, right, speed

		if self.firstGeneration:
			#Generate random DNA for the first generation
			self.DNAlength = (self.inputCount * self.neuronsPerLayer + self.neuronsPerLayer * 
				(self.numLayers - 1) + self.neuronsPerLayer * self.outputNeurons + 
				self.outputNeurons)
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
		self.weights = []
		self.count = 0
		self.l = np.array(self.DNA[self.count:self.count + self.numTiles*self.neuronsPerLayer])
		self.count += self.numTiles*self.neuronsPerLayer
		self.l = self.l.reshape(self.inputCount, self.neuronsPerLayer)
		self.weights.append(self.l)
		for i in range(self.numLayers - 1):
			self.l = np.array(self.DNA[self.count:self.count + self.neuronsPerLayer])
			self.count += self.neuronsPerLayer
			self.weights.append(l)
		self.l = np.array(self.DNA[self.count:self.count + self.outputNeurons*self.neuronsPerLayer])
		self.l = self.l.reshape(self.neuronsPerLayer, self.outputNeurons)
		self.weights.append(self.l)
		self.count += self.neuronsPerLayer * self.outputNeurons
		self.l = np.array(self.DNA[self.count:self.count + self.outputNeurons])
		self.weights.append(l)

		#Define Keras model of the brain, using sequential layers of activation neurons
		self.model = Sequential()
		self.model.add(Dense(self.neuronsPerLayer, input_shape = (self.inputCount,), activation='relu'))
		for i in range(self.numLayers - 1):
			self.model.add(Activation('relu'))
		self.model.add(Dense(self.outputNeurons, activation='relu'))
		self.model.set_weights(self.weights)
		self.model.add(Activation('relu'))

	def think(vision):
		#Use the creatures Keras model and vision to determine direction/speed
		self.actions = self.model.predict(vision)
		return self.actions