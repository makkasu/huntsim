"""
Name: feorh.py 
Authors: Oliver Giles & Max Potter
Date: June 2017
Description:
    - Use pygame to create a simplistic model of a tiger hunting deer
    - Randomly generate a tile-based map 
    - Populate the map with tigers and deer
    - Tigers and deer have neural network 'brains' that control their actions
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

#Open the output files
f = open('bestTigers.txt', 'w')
f2 = open('fitnessAndDeath.txt', 'w')
f.write("epoch,name,fitness,DNA\n")
f2.write("time,epoch,average fitness,average fitness of breeders,%wall deaths,killTotal\n")

def quit_game():
    f.close()
    pygame.quit()
    sys.exit()
    return

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

#Initialise tigers, then deers
print "Here come the tigers!"
for i in range(tigerPop):
    tempCreature = c.spawn_creature("tiger", mapHeight=height, mapWidth=width, tileSize=tileSize)
    print tempCreature[0].name

print "Meet the deer!"
for i in range(deerPop):
    tempCreature = c.spawn_creature("deer", mapHeight=height, mapWidth=width, tileSize=tileSize)
    print tempCreature[0].name
print "\n"

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
epochCounter = 0
timeCounter = 0
killTotal = 0
while not done:
    clock.tick(fps) # limit fps
    if not pause:
        #Detect collisions between each tiger and all the deer on the map. If there is a collision, kill the deer.
        for tiger in c.tigerList:
            collision_list = pygame.sprite.spritecollide(tiger, c.deerList, True)
            for col in collision_list:
                # print "%s was eaten by %s!" % (col.name.rstrip(), tiger.name.rstrip())
                tiger.eat(tigerEatEnergy)
                killTotal += 1

        #Gather all living sprites into one list
        cList = c.tigerList.sprites() + c.deerList.sprites()

        #Update creature vision
        for creature in cList:
            i, j = mf.find_tile(creature, tileSize, height, width)
            creature.get_vision(i, j, tilemap, height, width, tilemapMaster[i][j])
         
        #Handle input events
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for creature in cList:
                    if creature.rect.collidepoint(event.pos):
                        print creature.name.rstrip(), creature.energy
                        print "Vision: "
                        print "     %s" % (tileNames[creature.vision[0]])
                        print "  %s  %s  %s" % (tileNames[creature.vision[2]], tileNames[creature.vision[4]], tileNames[creature.vision[3]])
                        print "     %s" % (tileNames[creature.vision[1]])
            if event.type == pygame.KEYDOWN:
                if event.key == K_EQUALS:
                    c.deerSpeed += 1
                    print "Deer speed increased to %d" % c.deerSpeed
                if event.key == K_MINUS:
                    c.deerSpeed = c.deerSpeed - 1 if c.deerSpeed > 0 else 0
                    print "Deer speed decreased to %d" % c.deerSpeed
                if event.key == K_LEFTBRACKET:
                    fps = fps - 10 if fps >= 0 else 1
                    fps = fps if fps >= 1 else 1
                    print " * FPS = %d" % fps
                if event.key == K_RIGHTBRACKET:
                    fps += 10
                    print " * FPS = %d" % fps
                if event.key == K_SPACE:
                    print " * PAUSED * "
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

        #Kill any creature that walks off the map
        for creature in cList:
            if not displayRect.colliderect(creature.rect):
                # print "***********************              %s went off the map!" % (creature.name.rstrip())
                creature.die(deathByWall = True)

        #Update display
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
            #what tile is the creature on? If it stands on a tile not previously visted, update creature.tiles
            i, j = mf.find_tile(creature, tileSize, height, width)
            unique = True
            for t in creature.tiles:
                if i == t[0] and j == t[1]:
                    unique = False
                    break
            if unique:
                creature.tiles.append((i,j))

            #Update tilemap to reflect what creatures are on each tiles - tigers trump deer
            if creature.ctype == "tiger" and tilemapMaster[i][j] != wood: #tigers are invisible in the forest
                tigerPoints.append([i,j])
                tilemap[i][j] = tigerColour
            elif creature.ctype == "deer" and tilemap[i][j] != tigerColour: 
                tilemap[i][j] = deerColour
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

        #Diagnostics
        timeCounter += 1
        epochCounter += 1
        if epochCounter % 100 == 0:
            # find average fitness and dump it + wall deaths
            fitList = []
            for t in c.tigerList.sprites():
                fitList.append(t.calc_fitness())
            avFitness = sum(fitList) / len(fitList)
            avBreedingFitness = 0
            for t in c.bestTigerList:
                avBreedingFitness += t[2]
            avBreedingFitness = avBreedingFitness/len(c.bestTigerList) if len(c.bestTigerList) > 0 else 0.0
            wallDeathRate = 100 * sum(c.wallDeaths) / len(c.wallDeaths) if len(c.wallDeaths) > 0 else 0.0
            c.wallDeaths = 0
            f2.write("%d,%d,%f,%f,%f,%d\n" % (timeCounter,epochValue,avFitness,avBreedingFitness,wallDeathRate,killTotal))
        if epochCounter >= 2000: #End of epoch diagnostics
            #Dump current best tiger list 
            newTigerCount = 0
            for i,t in enumerate(c.bestTigerList):
                print "New tiger %s added to bestTigers.txt! Fitness = %d." % (t[1].rstrip(), t[2])
                f.write(str(t[0])+','+t[1].rstrip()+','+str(t[2])+','+t[3][0:100]+'\n')
                newTigerCount += 1
            ga.epochTigers = newTigerCount

            newDeerCount = 0
            for i,t in enumerate(c.bestTigerList):
                # print "New deer %s added to bestDeer.txt! Fitness = %d." % (t[1].rstrip(), t[2])
                # f.write(str(t[0])+','+t[1].rstrip()+','+str(t[2])+','+t[3][0:100]+'\n')
                newDeerCount += 1
            ga.epochDeers = newDeerCount

            c.bestTigerList = []
            c.bestDeerList = []
            epochCounter = 0
            epochValue += 1
            epochTime = time()
            c.epoch = epochValue
            print ' *                            Epoch:', epochValue

    else:
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    print " * RESUMED * "
                    pause = False
