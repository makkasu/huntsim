"""
Name: mapfuncs.py 
Authors: Oliver Giles & Max Potter
Date: June 2017
Description:
    - Use pygame to create a simplistic model of a tiger hunting deer
    - Randomly generate a tile-based map 
"""

import pygame
import sys
from pygame.locals import *
import mapfuncs as mf
import creatures as c

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
tileSize = 6 
height = 100
width = 150

#Create tilemap list
minSeeds = 50
maxSeeds = 50
tilemap = mf.create_map(width, height, minSeeds, maxSeeds)

#Initiate display
pygame.init()
display = pygame.display.set_mode((width * tileSize, height * tileSize))
pygame.display.set_caption('Hunt Sim')

#Initialise some deer at random locations
deer, deerSprite = c.spawn_deer(height, width, tileSize)

#Initialise a tiger
global tiger1
pos = [150,100]
tiger1 = c.Tiger(pos)
tigersprites = pygame.sprite.RenderPlain(tiger1)

#Draw the map
bgSurface = pygame.Surface(display.get_size())
for row in range(height):
    for column in range(width):
        bgRect = pygame.draw.rect(bgSurface, colours[tilemap[row][column]], (column*tileSize, row*tileSize, tileSize, tileSize))
bgSurface = bgSurface.convert()
display.blit(bgSurface,(0,0)) # blit the map to the screen

#Initialise clock
clock = pygame.time.Clock()

#Main game loop
done = False
while not done:
    clock.tick(10) # limit fps

    #Handle input events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_w:
                tiger1.moveup()
            if event.key == K_a:
                tiger1.moveleft()
            if event.key == K_s:
                tiger1.movedown()
            if event.key == K_d:
                tiger1.moveright()
        elif event.type == KEYUP:
            tempTarget = tiger1.target
            #tiger1.target = [0,0]
            #tiger1.state = "stopped"

            if event.key == K_w or event.key == K_s:
                tiger1.target[1] = 0
            if event.key == K_a or event.key == K_d:
                tiger1.target[0] = 0


    #Update display
    display.blit(bgSurface, tiger1.rect, tiger1.rect)
    tigersprites.update()
    tigersprites.draw(display)
    pygame.display.flip()
    pygame.display.update()