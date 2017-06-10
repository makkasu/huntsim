"""
Name: minds.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains creatures' neural networks
"""

import tensorflow as tf
import random
import numpy as np

class Mind():
	def __init__(self, numTiles, neuronsPerLayer, numLayers, firstGeneration, DNA):
		self.inputNeurons = numTiles
		self.outputNeurons = 5 #up, down, left, right, speed

		if firstGeneration:
			#Create numpy.ndarrays with random weights/biases between layers
			self.l1Weights = 
			self.l1Biases = 
			self.l2Weights = 
			self.l2Biases = 
			self.outWeights =
			self.outBiases =

		else:
			#Convert DNA to numpy.ndarrays

		self.DNA = '' #All floats of all tensors converted into a string of bits

def think(tiles, DNA):
	#Use the creatures DNA to construct tensors of weights/biases and feed tiles through
	pass

