"""
Name: creatures.py 
Author: Oliver Giles & Max Potter
Date: May 2017
Description:
	- Contains class definitions for the animals of the game
"""

import pygame
from pygame.locals import *

def load_png(name):
	image = pygame.image.load(name)
	if image.get_alpha is None:
		image = image.convert()
	else:
		image = image.convert_alpha()
	return image, image.get_rect()


class Tiger(pygame.sprite.Sprite):
    """
    Tigers hunt deer
    """

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('tiger.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 1
        self.state = "stopped"
        self.rect = self.image.get_rect(topleft=(position[0], position[1]))
        self.target = [0, 0]

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