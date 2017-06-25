"""
Name: constants.py 
Authors: Oliver Giles & Max Potter
Date: June 2017
Description:
    - Stores the various parameters of the game
"""

#Constants for colours
orange = (242, 68, 56)
yellow = (255,193,8)
brown =(120, 84, 72)
green =(76, 173, 80)
white = (255, 255, 255)

#Constants for tiles
dirt = 0
grass = 1
wood = 2
deer = 3
tiger = 4

#Colour to tile conversion
colours = {
            dirt : white,
            grass : green,
            wood : brown,
            deer : yellow,
            tiger : orange
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