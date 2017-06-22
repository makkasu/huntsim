"""
Name: creatures.py 
Author: Oliver Giles & Max Potter
Date: June 2017
Description:
	- Contains class definitions for the animals of the game
"""

import pygame
from pygame.locals import *
from random import randint

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

    def __init__(self, position, ctype):
        pygame.sprite.Sprite.__init__(self)
        self.ctype = ctype

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

        #Vision
        self.vision = [[-1 for column in range(5)] for row in range(5)]

    def update(self):
        self.energy -= self.drainRate
        if self.energy <= 0:
            if self.ctype == 'tiger':
                tigerList.remove(self)
            if self.ctype == 'deer':
                deerList.remove(self)

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        pygame.event.pump()

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
