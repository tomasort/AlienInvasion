import pygame
from sys import exit
from time import sleep 

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button 

class AlienInvasion:
    """Oveall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # pygame.init() initializes the background settings.
        self.settings = Settings()
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(self.settings.screen_size) # Create a display window.
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics. 
        self.stats = GameStats(self) 
        self.ship = Ship(self)
        self.play_button = Button(self, 'Play')
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of alines."""
        # create an alien and find the number of aliens in a row
        # spacing between each alien is equal to one alien width. 
        alien = Alien(self)
        alien_width = alien.rect.width 
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen. 
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create all the rows of the fleet of aliens 
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the correspoding position on the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.alien_direction *= -1
        print("The velocity of the aliens is {}".format(self.settings.alien_speed))

    def fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_q:
            exit()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_events(self):
        """ Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Checks if the play button has been pressed"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Reset the game settings and stats
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            # Remove existing aliens and bullets 
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and then center the ship
            self._create_fleet()
            self.ship.center_ship()

    def _update_screen(self):
        """ Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet() 
        self.aliens.draw(self.screen)
        if not self.stats.game_active: 
            self.play_button.draw_button() 
        pygame.display.flip()

    def _update_aliens(self):
        """Update the position of the aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions. 
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit() 
        self._check_alien_invasion()
    
    def _ship_hit(self): 
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0: 
            self.stats.ships_left -= 1 # remove one ship
            # Get rid of any remaining aliens and bullets. 
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship. 
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else: 
            self.stats.game_active = False

    def _check_alien_invasion(self):
        """Chack if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites(): 
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien  collisions."""
        # Remove any bullets and aliens that have collided
        # To make a bullet that destroys multiple aliens set the first boolean to False and the second to True
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens: 
            self._create_fleet()
            self.settings.increase_speed()

    def run_game(self):
        """Atart the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active: 
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    #TODO: add buttons for changing the dificulty of the levels in the game. 

if __name__ == '__main__':
    # Make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()