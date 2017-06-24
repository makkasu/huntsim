"""
Name: minds.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains creatures' neural networks
"""

from keras.models import Sequential
from keras.layers import Activation, Dense
import random
import numpy as np
import math
from bitstring import BitArray

class Mind():
	def __init__(self, numTiles=25, neuronsPerLayer=50, numLayers=2, firstGeneration=False, DNA=''):
		self.inputCount = numTiles
		self.neuronsPerLayer = neuronsPerLayer
		self.firstGeneration = firstGeneration
		self.numLayers = numLayers
		self.DNA = DNA
		self.outputNeurons = 5 #up, down, left, right, speed

		if self.firstGeneration:
			#Generate random DNA for the first generation
			self.DNAlength = (self.inputCount * self.neuronsPerLayer + self.neuronsPerLayer * 
				(self.numLayers - 1) + self.neuronsPerLayer * self.outputNeurons + 
				self.outputNeurons)
			self.DNAbin = []
			for i in range(0, self.DNAlength * 32):
				self.DNAbin.append(str(random.randint(0,1)))
			self.b = BitArray(float=0.00, length=32)
			self.DNAbin = ''.join(self.DNAbin)

			self.DNA = []
			for i in range(0, len(self.DNAbin), 32):
				self.b.bin = self.DNAbin[i:i+32]
				self.DNA.append([0.0 if math.isnan(self.b.float) else self.b.float])

		#Convert DNA to weights
		self.weights = []
		self.count = 0
		self.l = np.array(self.DNA[self.count:self.count + self.inputCount*self.neuronsPerLayer])
		self.count += self.inputCount*self.neuronsPerLayer
		self.l = self.l.reshape(self.inputCount, self.neuronsPerLayer)
		self.weights.append(self.l)
		for i in range(self.numLayers - 1):
			self.l = np.array(self.DNA[self.count:self.count + self.neuronsPerLayer])
			self.l = self.l.reshape(self.neuronsPerLayer)
			self.count += self.neuronsPerLayer
			self.weights.append(self.l)
		self.l = np.array(self.DNA[self.count:self.count + self.outputNeurons*self.neuronsPerLayer])
		self.l = self.l.reshape(self.neuronsPerLayer, self.outputNeurons)
		self.weights.append(self.l)
		self.count += self.neuronsPerLayer * self.outputNeurons
		self.l = np.array(self.DNA[self.count:self.count + self.outputNeurons])
		self.l = self.l.reshape(self.outputNeurons)
		self.weights.append(self.l)

		#Define Keras model of the brain, using sequential layers of activation neurons
		self.model = Sequential()
		self.model.add(Dense(self.neuronsPerLayer, input_shape = (self.inputCount,), activation='relu'))
		for i in range(self.numLayers - 1):
			self.model.add(Activation('relu'))
		self.model.add(Dense(self.outputNeurons, activation='relu'))
		self.model.add(Activation('relu'))
		print self.weights
		for arr in self.model.get_weights():
			print arr
			print arr.shape
		for arr in self.weights:
			#print arr
			print arr.shape
		#self.model.set_weights(self.weights)

	def think(self, vision):
		#Use the creatures Keras model and vision to determine direction/speed
		vision = np.array([[element for sublist in vision for element in sublist]])
		self.actions = self.model.predict(vision)
		print self.actions
		return self.actions