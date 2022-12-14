import pygame

class Ship:
    """ A class to manage the ship. """

    def __init__(self, ai_game):
        """ Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() # get the rectangular area of the game screen

        # Load the ship image and get its rect. 
        self.image = pygame.image.load('images/rocket.bmp') # surface representing the ship
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen. 
        self.rect.midbottom = self.screen_rect.midbottom 
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.settings = ai_game.settings

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += int(self.settings.ship_speed)
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= int(self.settings.ship_speed)
        if self.moving_up:
            self.rect.y -= self.settings.ship_speed
        if self.moving_down:
            self.rect.y += self.settings.ship_speed

    def blitme(self):
        """ Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)