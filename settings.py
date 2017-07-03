"""
Name: settings.py 
Authors: Oliver Giles & Max Potter
Date: June 2017
Description:
    - Stores the various parameters of the game
"""
from numpy import float32

#Starting framerate
fps = 10

#Constants for colours
orange = (242, 68, 56)
yellow = (255,193,8)
brown = (120, 84, 72)
green = (76, 173, 80)
white = (255, 255, 255)

#Constants for tiles
wall = float32(-1.0)
dirt = float32(-0.6)
grass = float32(-0.2)
wood = float32(0.2)
tigerColour = float32(0.6)
deerColour = float32(1.0)

#Colour to tile conversion
colours = {
            dirt : white,
            grass : green,
            wood : brown,
            deerColour : yellow,
            tigerColour : orange
          }
          
#Game dimensions
tileSize = 30 
height = 20
width = 30

#Tilemap parameters
minSeeds = 50
maxSeeds = 50

#Energy gained by eating deer or grass
tigerEatEnergy = 50
deerEatEnergy = 3