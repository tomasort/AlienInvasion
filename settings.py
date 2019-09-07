class Settings: 
    """ A class to store all the settings for the alien invasion game"""

    def __init__(self):
        """ Initialize the game's settings"""
        # First we go through the screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.screen_size = self.screen_width, self.screen_height
        self.ship_speed = 8.5