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

def load_png(name):
	image = pygame.image.load(name)
	if image.get_alpha is None:
		image = image.convert()
	else:
		image = image.convert_alpha()
	return image, image.get_rect()

class Creature():
    """
    Parent class for all creatures.
    Handles movement. 
    Child classes handle sprites & behaviours.
    """

    def __init__(self):
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 1
        self.state = "stopped"
        self.target = [0,0]

    def update(self):
        newpos = self.rect.move(self.target)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.target[1] = self.target[1] - (self.speed)
        self.state = "up"

    def movedown(self):
        self.target[1] = self.target[1] + (self.speed)
        self.state = "down"

    def moveleft(self):
        self.target[0] = self.target[0] - (self.speed)
        self.state = "left"

    def moveright(self):
        self.target[0] = self.target[0] + (self.speed)
        self.state = "right"


class Tiger(Creature, pygame.sprite.Sprite):
    """
    Tigers hunt deer
    Inherits from creatures
    Handles sprite initialisation
    """

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('tiger.png')
        super(Tiger,self).__init__() # complete the rest of creature initialisation
        self.rect = self.image.get_rect(topleft=(position[0], position[1]))
        #self.add(tigerList)

class Deer(Creature, pygame.sprite.Sprite):
    """
    Deer eat grass
    Inherits from creatures
    Handles sprite initialisation
    """

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('deer.png')
        super(Deer,self).__init__() # complete the rest of creature initialisation
        self.rect = self.image.get_rect(topleft=(position[0], position[1]))
        #self.add(deerList)


def spawn_deer(height, width, tilesize):
    """
    Generates random location and initialises instance of Deer object.
    Returns a deer object & sprite.
    """
    rangeX = width*tilesize
    rangeY = height*tilesize
    pos = [randint(0,rangeX), randint(0,rangeY)]
    deer = Deer(pos)
    deerSprite = pygame.sprite.RenderPlain(deer)

    return deer, deerSprite