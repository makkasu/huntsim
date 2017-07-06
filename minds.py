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

class Mind():
	def __init__(self, numTiles=6, neuronsPerLayer=15, numLayers=1, firstGeneration=False, DNA=''):
		self.inputCount = numTiles
		self.neuronsPerLayer = neuronsPerLayer
		self.firstGeneration = firstGeneration
		self.numLayers = numLayers
		self.DNA = DNA
		self.outputNeurons = 4 #up, down, left, right (speed is gone for now)

		if self.firstGeneration:
			#Generate random DNA for the first generation
			self.DNAlength = (self.inputCount * self.neuronsPerLayer + self.neuronsPerLayer +
				((self.neuronsPerLayer * self.neuronsPerLayer) * self.numLayers) + self.neuronsPerLayer * 
				self.outputNeurons + self.neuronsPerLayer * self.numLayers + self.outputNeurons)
			self.DNAbin = []
			for i in range(0, self.DNAlength * 12):
				self.DNAbin.append(str(random.randint(0,1)))
			
			self.DNAbin = ''.join(self.DNAbin)
			self.b = BitArray(int=0, length=12)
			self.DNA = []
			for i in range(0, len(self.DNAbin), 12):
				self.b.bin = self.DNAbin[i:i+12]
				self.DNA.append(float(self.b.int))
		else:
			self.DNAbin = self.DNA
			self.DNA = []
			self.b = BitArray(int=0, length=12)
			for i in range(0, len(self.DNAbin), 12):
				self.b.bin = self.DNAbin[i:i+12]
				self.DNA.append(float(self.b.int))

		#Convert DNA to list of weights
		self.weights = []
		self.count = 0
		#Normalise our converted DNA to floats between -0.5 and 0.5
		self.DNA = 2*(self.DNA-np.float32(-2048))/(np.float32(2047)-np.float32(-2048)) - 1

		#Convert list of weights into shaped arrays for each layer
		#Input weights: inputCount x neuronsPerLayer matrix
		self.l = np.array(self.DNA[self.count:self.count + self.inputCount*self.neuronsPerLayer])
		self.count += self.inputCount*self.neuronsPerLayer
		self.l = self.l.reshape(self.inputCount, self.neuronsPerLayer)
		self.weights.append(self.l)
		#Input activation weights: neuronsPerLayer array
		self.l = np.array(self.DNA[self.count:self.count + self.neuronsPerLayer])
		self.count += self.neuronsPerLayer
		self.l = self.l.reshape(self.neuronsPerLayer)
		self.weights.append(self.l)

		for i in range(self.numLayers):
			#Hidden layer weights: neuronsPerLayer x neuronsPerLayer matrix
			self.l = np.array(self.DNA[self.count:self.count + self.neuronsPerLayer*self.neuronsPerLayer])
			self.count += self.neuronsPerLayer*self.neuronsPerLayer
			self.l = self.l.reshape(self.neuronsPerLayer, self.neuronsPerLayer)
			self.weights.append(self.l)
			#Hidden activation weights: neuronsPerLayer array
			self.l = np.array(self.DNA[self.count:self.count + self.neuronsPerLayer])
			self.count += self.neuronsPerLayer
			self.l = self.l.reshape(self.neuronsPerLayer)
			self.weights.append(self.l)
		
		#Output layer weights: neuronsPerLayer x outputNeruons matrix
		self.l = np.array(self.DNA[self.count:self.count + self.outputNeurons*self.neuronsPerLayer])
		self.l = self.l.reshape(self.neuronsPerLayer, self.outputNeurons)
		self.weights.append(self.l)
		self.count += self.neuronsPerLayer * self.outputNeurons
		#Hidden activation weights: neuronsPerLayer array
		self.l = np.array(self.DNA[self.count:self.count + self.neuronsPerLayer])
		self.count += self.neuronsPerLayer
		self.l = self.l.reshape(self.outputNeurons)
		self.weights.append(self.l)

		#Define Keras model of the brain, using sequential layers of 'relu' activation neurons
		#and the weights as structured above
		self.model = Sequential()
		self.model.add(Dense(self.neuronsPerLayer, input_shape = (self.inputCount,), activation='relu'))
		for i in range(self.numLayers):
			self.model.add(Dense(self.neuronsPerLayer, activation='relu'))
		self.model.add(Dense(self.outputNeurons, activation='relu'))
		self.model.set_weights(self.weights)

	def think(self, vision):
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
		self.actions = self.model.predict(vision2)
		return self.actions