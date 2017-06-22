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
from copy import deepcopy

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

#Create tilemap list
minSeeds = 50
maxSeeds = 50
tilemap = mf.create_map(width, height, minSeeds, maxSeeds)
tilemapMaster = deepcopy(tilemap) #edits to sub arrays in tilemap won't edit tilemapMaster

#Lists of objects
tigerList = pygame.sprite.Group()
deerList = pygame.sprite.Group()

#Energy gained by eating deer or grass
tigerEatEnergy = 50
deerEatEnergy = 3

#Initiate display
pygame.init()
display = pygame.display.set_mode((width * tileSize, height * tileSize))
displayRect = display.get_rect()
pygame.display.set_caption('Hunt Sim')

#Draw the map
bgSurface = pygame.Surface(display.get_size())
for row in range(height):
    for column in range(width):
        bgRect = pygame.draw.rect(bgSurface, colours[tilemap[row][column]], (column*tileSize, row*tileSize, tileSize, tileSize))
bgSurface = bgSurface.convert()
display.blit(bgSurface,(0,0)) # blit the map to the screen

#Initialise some deer at random locations
for i in range(10):
    c.spawn_creature("deer", mapHeight=height, mapWidth=width, tileSize=tileSize)

#Initialise a tiger
tiger1, tigersprites = c.spawn_creature("tiger", pos=[150,100])

#Initialise blank lists for previous tiger and deer positions on the map
oldDeerPoints = []
oldTigerPoints = []

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
            tiger.eat(tigerEatEnergy)

    #Gather all living sprites into one list
    cList = c.tigerList.sprites() + c.deerList.sprites()
    #Update creature vision
    for creature in cList:
        i, j = mf.find_tile(creature, tileSize, height, width)
        creature.vision = mf.get_vision(i, j, tilemap, height, width)
        if creature.ctype == "tiger":
            print '\n'
            print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in creature.vision]))
     

    #Handle input events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        tiger1.speed = tiger1.topSpeed
    else:
        tiger1.speed = tiger1.baseSpeed
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_w:
                tiger1.dy -= 1
            if event.key == K_a:
                tiger1.dx -= 1
            if event.key == K_s:
                tiger1.dy += 1
            if event.key == K_d:
                tiger1.dx += 1
        elif event.type == KEYUP:
            if event.key == K_w or event.key == K_s:
                tiger1.dy = 0
            if event.key == K_a or event.key == K_d:
                tiger1.dx = 0

    #Update display
    #Blit all living sprites on top of the background
    for creature in cList:
        creature.rect.clamp_ip(displayRect)
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

    #Update tilemap with positions of all creatures
    tigerPoints = []
    deerPoints = []
    for creature in cList:
        #what tile is the creature on?
        i, j = mf.find_tile(creature, tileSize, height, width)

        #Update tilemap to reflect what creatures are on each tiles - tigers trump deer
        if creature.ctype == "tiger" and tilemapMaster != wood: #tigers are invisible in the forest
            tigerPoints.append([i,j])
            tilemap[i][j] = 4
        elif creature.ctype == "deer" and tilemap[i][j] != tiger: 
            tilemap[i][j] = 3
            deerPoints.append([i,j])
            if tilemapMaster[i][j] == grass: #don't forget to feed the deer!
                creature.eat(deerEatEnergy)

    #Gather list of empty tiles by comparing old and new lists, then replace the tiles with their original types.
    emptyTiles = [point for point in oldTigerPoints if point not in tigerPoints]
    emptyTiles.extend([point for point in oldDeerPoints if point not in deerPoints])
    for tile in emptyTiles:
        tilemap[tile[0]][tile[1]] = tilemapMaster[tile[0]][tile[1]]

    oldDeerPoints = deerPoints
    oldTigerPoints = tigerPoints
