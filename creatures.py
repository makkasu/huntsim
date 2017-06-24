"""
Name: creatures.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains class definitions for the animals of the game
"""

import pygame
from pygame.locals import *
from random import randint, choice
import minds as m

#Lists of objects
tigerList = pygame.sprite.Group()
deerList = pygame.sprite.Group()

def load_png(name):
	image = pygame.image.load(name)
	if image.get_alpha is None:
		image = image.convert()
	else:
		image = image.convert_alpha()
	return image, image.get_rect()

class Creature(pygame.sprite.Sprite):
    """
    Generic creature class.
    Tigers hunt deer, deer eat grass. 
    All creatures lose energy over time and die it if hits zero.
    Handles sprite initialisation and movement.
    """

    def __init__(self, position, ctype, DNA = ''):
        pygame.sprite.Sprite.__init__(self)
        self.ctype = ctype
        self.name = self.get_name()

        #Handle creature type senstive parameters
        if ctype == 'tiger':
            self.image, self.rect = load_png('tiger.png')
            self.add(tigerList)
            self.baseSpeed = 2
            self.topSpeed = 10
            self.energy = 1500
            self.drainRate = 1
        elif ctype == 'deer':
            self.image, self.rect = load_png('deer.png')
            self.add(deerList)
            self.baseSpeed = 2
            self.topSpeed = 3
            self.energy = 1000
            self.drainRate = 2

        #Set up display information
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()  
        self.rect = self.image.get_rect(topleft=(position[0], position[1]))
        
        #Movement
        self.speed = self.baseSpeed
        self.dx = 0
        self.dy = 0

        #Set up default vision (5x5 grid, all seeing 'off map')
        self.vision = [[-1 for column in range(5)] for row in range(5)]

        #Create blank DNA and attach a Mind object to our creature
        self.DNA = DNA
        child = False if len(self.DNA) > 0 else True #children will have non-blank DNA strings
        self.mind = m.Mind(firstGeneration = child, DNA = DNA)

    def update(self):
        #Deplete energy and check if still alive!
        self.energy -= self.drainRate
        if self.energy <= 0:
            if self.ctype == 'tiger':
                #*********************************************PASS ON DNA!!!!
                tigerList.remove(self)
            if self.ctype == 'deer':
                #*********************************************PASS ON DNA!!!!
                deerList.remove(self)

        #Feed vision into neural network and retrieve button presses
        actions = self.mind.think(self.vision)

        for action in actions: 
            #Speed up: action[0] = K_SPACE
            if int(round(action[0])) == 1:
                self.speed = self.topSpeed
            else:
                self.speed = self.baseSpeed

            left, right, up, down, speed = False, False, False, False, False
            self.dx, self.dy = 0, 0 #Reset speed

            #Establish 'buttons pressed': 
            if int(round(action[1])) == 1: #action[1] = K_w
                up = True
            if int(round(action[2])) == 1: #action[2] = K_a
                left = True
            if int(round(action[3])) == 1: #action[2] = K_s
                down = True
            if int(round(action[4])) == 1: #action[2] = K_d
                right = True

            if up and not down:
                self.dy = 1
            if down and not up:
                self.dy = -1
            if left and not right:
                self.dx = -1
            if right and not left:
                self.dx = 1

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        pygame.event.pump()

    def get_name(self):
        return choice(list(open('names.txt')))

    def eat(self, eatEnergy):
        self.energy += eatEnergy


def spawn_creature(ctype, mapHeight = 100, mapWidth = 150, tileSize = 6, pos=[-1,-1]):
    """
    Initialises instance of a creature of type ctype.
    In absence of pos argument, spawn location is randomly generated based on height & width.
    Returns an object and a sprite.
    """
    #if pos is unchanged by user then randomly generate a position
    if pos == [-1,-1]: 
        rangeX = (mapWidth-1)*tileSize
        rangeY = (mapHeight-1)*tileSize
        pos = [randint(0,rangeX), randint(0,rangeY)]
    
    #if pos argument is passed but invalid, make it [0,0]
    if pos[0] < 0 and pos[1] < 0: 
        pos = [0,0]

    newCreature = Creature(pos, ctype)
    newSprite = pygame.sprite.RenderPlain(newCreature)

    return newCreature, newSprite
