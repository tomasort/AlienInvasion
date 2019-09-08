class Settings: 
    """ A class to store all the settings for the alien invasion game"""

    def __init__(self):
        """ Initialize the game's settings"""
        # First we go through the screen settings
        self.fullscreen = False
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (255, 255, 255)
        self.screen_size = self.screen_width, self.screen_height

        # Ship settings
        self.ship_speed = 8.5

        # Bullet settings 
        self.bullet_speed = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_width = 3
        self.bullet_height = 15