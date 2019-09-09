class Settings: 
    """ A class to store all the settings for the alien invasion game"""

    def __init__(self):
        """ Initialize the game's settings"""
        # First we go through the screen settings
        self.fullscreen = False
        self.screen_width = 700
        self.screen_height = 600
        self.bg_color = (255, 255, 255)
        self.screen_size = self.screen_width, self.screen_height

        # Ship settings
        self.ship_limit = 3

        # Bullet settings 
        self.bullet_color = (60, 60, 60)
        self.bullet_width = 3
        self.bullet_height = 15

        # Alien settings
        self.alien_drop_speed = 3

        # How quickly the game speeds up 
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings() 
        self.alien_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale * 5

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 3.5
        self.bullet_speed = 15.0
        self.alien_speed = 0.5

        # fleet_direction of 1 represents right; -1 represents left. 
        self.alien_direction = 1
