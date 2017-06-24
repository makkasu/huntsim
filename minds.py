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
	def __init__(self, numTiles=25, neuronsPerLayer=20, numLayers=2, firstGeneration=False, DNA=''):
		self.inputCount = numTiles
		self.neuronsPerLayer = neuronsPerLayer
		self.firstGeneration = firstGeneration
		self.numLayers = numLayers
		self.DNA = DNA
		self.outputNeurons = 5 #up, down, left, right, speed

		if self.firstGeneration:
			#Generate random DNA for the first generation
			self.DNAlength = (self.inputCount * self.neuronsPerLayer + self.neuronsPerLayer +
				((self.neuronsPerLayer * self.neuronsPerLayer) * self.numLayers) + self.neuronsPerLayer * 
				self.outputNeurons + self.neuronsPerLayer * self.numLayers + self.outputNeurons)
			self.DNAbin = []
			for i in range(0, self.DNAlength * 12):
				self.DNAbin.append(str(random.randint(0,1)))
			self.b = BitArray(int=0, length=12)
			self.DNAbin = ''.join(self.DNAbin)

			self.DNA = []
			for i in range(0, len(self.DNAbin), 12):
				self.b.bin = self.DNAbin[i:i+12]
				self.DNA.append([float(self.b.int) if math.isnan(self.b.int) else float(self.b.int)]) 
				#Currently does nothing - replace first word with 1

		#Convert DNA to weights
		self.weights = []
		self.count = 0
		self.DNA = (self.DNA-np.amin(self.DNA))/(np.amax(self.DNA)-np.amin(self.DNA)) - 0.5 #TEST NORMALISATION - SEEMS TO WORK

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


		#Define Keras model of the brain, using sequential layers of activation neurons
		self.model = Sequential()
		self.model.add(Dense(self.neuronsPerLayer, input_shape = (self.inputCount,), activation='sigmoid'))
		for i in range(self.numLayers):
			self.model.add(Dense(self.neuronsPerLayer, activation='sigmoid'))
		self.model.add(Dense(self.outputNeurons, activation='sigmoid'))
		#print self.weights
		for arr in self.model.get_weights():
			#print arr
			#print arr.shape
			pass
		for arr in self.weights:
			print arr
			#print arr.shape
			pass
		# weights = []
		# # # weights.append(np.random.rand(25, 20))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (25, 20)))
		# #weights.append(np.zeros(20,))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (20,)))
		# # # weights.append(np.random.rand(20, 20))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (20, 20)))
		# #weights.append(np.zeros(20,))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (20,)))
		# # # weights.append(np.random.rand(20, 20))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (20, 20)))
		# #weights.append(np.zeros(20,))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (20,)))
		# # # weights.append(np.random.rand(20, 5))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (20, 5)))
		# #weights.append(np.zeros(5,))
		# weights.append(np.random.uniform(low = -1, high = 1.0, size = (5,)))
		self.model.set_weights(self.weights)

	def think(self, vision):
		#Use the creatures Keras model and vision to determine direction/speed
		vision = np.array([[element for sublist in vision for element in sublist]])
		self.actions = self.model.predict(vision)
		#print self.actions
		return self.actions