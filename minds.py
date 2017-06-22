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

class Mind():
	def __init__(self, numTiles=25, neuronsPerLayer=50, numLayers=3, firstGeneration, DNA):
		self.inputCount = numTiles
		self.outputNeurons = 5 #up, down, left, right, speed

		if firstGeneration:
			#Create numpy.ndarrays with random weights/biases between layers
			self.l1Weights = 
			self.l1Biases = 
			self.l2Weights = 
			self.l2Biases = 
			self.outWeights =
			self.outBiases =
			self.DNA = '' #All floats of all tensors converted into a string of bits
		else:
			#Convert DNA to weights/biases

		#Define Keras model of the brain, using sequential layers of activation neurons
		#Set weights using DNA : https://keras.io/models/about-keras-models/
		model = Sequential()
		model.add(Dense(neuronsPerLayer, input_shape = (inputCount,)))
		model.add(Activation('relu'))
		for i in range(numLayers - 1):
			model.add(Dense(neuronsPerLayer))
			model.add(Activation('relu'))
		model.add(Dense(outputNeurons))
		model.add(Activation('relu'))

def think(mind, vision):
	#Use the creatures Keras model and vision to determine direction/speed
	actions = mind.predict(vision)
	return actions