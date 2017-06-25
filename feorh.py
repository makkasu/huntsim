"""
Name: feorh.py 
Authors: Oliver Giles & Max Potter
Date: June 2017
Description:
    - Use pygame to create a simplistic model of a tiger hunting deer
    - Randomly generate a tile-based map 
    - Populate the map with tigers and deer
    - Tigers and deer have neural network 'brains' with 65 neurons each
"""

import pygame
import sys
from pygame.locals import *
import mapfuncs as mf
import creatures as c
import genetic_algorithm as ga
from copy import deepcopy
from settings import * #Various constants (such as the game dimensions) are stored here to reduce clutter
from time import time

#Create tilemap list
tilemap = mf.create_map(width, height, minSeeds, maxSeeds)
tilemapMaster = deepcopy(tilemap) #edits to sub arrays in tilemap won't edit tilemapMaster

#Initiate display
pygame.init()
display = pygame.display.set_mode((width * tileSize, height * tileSize))
displayRect = display.get_rect()
pygame.display.set_caption('Feorh')

#Draw the map
bgSurface = pygame.Surface(display.get_size())
for row in range(height):
    for column in range(width):
        bgRect = pygame.draw.rect(bgSurface, colours[tilemap[row][column]], (column*tileSize, row*tileSize, tileSize, tileSize))
bgSurface = bgSurface.convert()
display.blit(bgSurface,(0,0)) # blit the map to the screen

#Initialise some deer at random locations
deerPop = 10
tigerPop = 5

print "Meet the deer!"
for i in range(deerPop):
    tempCreature = c.spawn_creature("deer", mapHeight=height, mapWidth=width, tileSize=tileSize)
    print tempCreature[0].name
print "\n"

#Initialise a tiger
print "And here come the tigers!"
for i in range(tigerPop):
    tempCreature = c.spawn_creature("tiger", mapHeight=height, mapWidth=width, tileSize=tileSize)
    print tempCreature[0].name

#Initialise blank lists for previous tiger and deer positions on the map
oldDeerPoints = []
oldTigerPoints = []

#Initialise clock
clock = pygame.time.Clock()

#Initiliase epoch count
epochValue = 1
epochTime = time()

#Main game loop
done = False
pause = False
while not done:
    clock.tick(fps) # limit fps

    if not pause:
        #Detect collisions between each tiger and all the deer on the map. If there is a collision, kill the deer.
        for tiger in c.tigerList:
            collision_list = pygame.sprite.spritecollide(tiger, c.deerList, True)
            for col in collision_list:
                print "%s was eaten by %s!" % (col.name.rstrip(), tiger.name.rstrip())
                tiger.eat(tigerEatEnergy)

        #Gather all living sprites into one list
        cList = c.tigerList.sprites() + c.deerList.sprites()

        #Update creature vision
        for creature in cList:
            i, j = mf.find_tile(creature, tileSize, height, width)
            creature.vision = mf.get_vision(i, j, tilemap, height, width)
            creature.vision[2][2] = tilemapMaster[i][j] #stop the tiger seeing itself in the centre square
            # if creature.ctype == "tiger":
            #     print '\n'
            #     print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in creature.vision]))
         
        #Handle input events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for creature in cList:
                    if creature.rect.collidepoint(event.pos):
                        print creature.name.rstrip(), creature.energy
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFTBRACKET:
                    fps = fps - 10 if fps >= 0 else 1
                    print " * FPS = %d" % fps
                if event.key == K_RIGHTBRACKET:
                    fps += 10
                    print " * FPS = %d" % fps
                if event.key == K_SPACE:
                    pause = True

        #Check if there are enough tigers and deers. If not, create children
        if len(c.tigerList) < tigerPop:
            if len(ga.tGenepool) < 15:
                c.spawn_creature("tiger", mapHeight=height, mapWidth=width, tileSize=tileSize)
                pass
            else:
                if len(ga.tPregnancies) > 0:
                    DNA = ga.get_DNA("tiger")
                    c.spawn_creature("tiger", mapHeight=height, mapWidth=width, tileSize=tileSize, DNA=DNA)
                else:
                    ga.breed("tiger")
                    DNA = ga.get_DNA("tiger")
                    c.spawn_creature("tiger", mapHeight=height, mapWidth=width, tileSize=tileSize, DNA=DNA)

        if len(c.deerList) < deerPop:
            if len(ga.dGenepool) < 15:
                c.spawn_creature("deer", mapHeight=height, mapWidth=width, tileSize=tileSize)
            else:
                if len(ga.dPregnancies) > 0:
                    DNA = ga.get_DNA("deer")
                    c.spawn_creature("deer", mapHeight=height, mapWidth=width, tileSize=tileSize, DNA=DNA)
                else:
                    ga.breed("deer")
                    DNA = ga.get_DNA("deer")
                    c.spawn_creature("deer", mapHeight=height, mapWidth=width, tileSize=tileSize, DNA=DNA)

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

        #Update epoch if necessary
        if time() - epochTime >= 200:
            epochValue += 1
            epochTime = time()
            c.epoch = epochValue
            print 'Epoch:', epochValue

    else:
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    pause = False
