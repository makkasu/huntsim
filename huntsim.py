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

#Lists of objects
tigerList = pygame.sprite.Group()
deerList = pygame.sprite.Group()

#Energy gained by eating deer or grass
tigerEatEnergy = 50
deerEatEnergy = 1

#Initiate display
pygame.init()
display = pygame.display.set_mode((width * tileSize, height * tileSize))
pygame.display.set_caption('Hunt Sim')

#Initialise some deer at random locations
c.spawn_creature(height, width, tileSize, "deer")

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

    for tiger in c.tigerList:
        #Detect collisions between each tiger and all the deer on the map. If there is a collision, kill the deer.
        collision_list = pygame.sprite.spritecollide(tiger, c.deerList, True)

        for col in collision_list:
            #Give tiger energy
            tiger.energy += tigerEatEnergy

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
            if event.key == K_w or event.key == K_s:
                tiger1.target[1] = 0
            if event.key == K_a or event.key == K_d:
                tiger1.target[0] = 0

    #Update display
    # - gather all living sprites into one list and blit them on top of the background
    cList = c.deerList.sprites() + c.tigerList.sprites()
    #update background to cover up dead (unupdated) sprites
    display.blit(bgSurface,(0,0))
    for creature in cList:
        display.blit(bgSurface, creature.rect, creature.rect)  
    c.deerList.update()
    c.tigerList.update()
    # - draw all living sprites to the screen
    c.deerList.draw(display)
    c.tigerList.draw(display)
    pygame.display.update()