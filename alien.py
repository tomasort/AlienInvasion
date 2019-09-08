import pygame 
from random import random, randint
from math import isclose
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien"""

    def __init__(self, ai_game):
        """Initialize the Alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

#        # load the aline image and set its rect attribute. 
#        if random() < 0.3:
#            self.image = pygame.image.load('images/monster-big.bmp')
#        else:
#            self.image = pygame.image.load('images/monster-small.bmp')
        self.image = pygame.image.load('images/monster-small.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = randint(self.screen_rect.left, self.screen_rect.right)
        self.rect.y = randint(0, self.screen_rect.bottom - self.rect.height)     # Store the alien's exact horizontal position. 
        self.x = float(self.rect.x)
        

