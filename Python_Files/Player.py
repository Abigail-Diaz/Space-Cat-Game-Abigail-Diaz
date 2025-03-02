from Sprites import Sprite
from Physics import Physics
from Counter import Counter
import pygame as pg

class Player(Sprite):
    '''Manages player's animation and physics '''
    def __init__(self, posx, posy, image_width, image_length, level, screen):
        self.level = level
        self.screen = screen
        self.visible = False
        self.initial_posx = 120
        self.initial_posy = 270
        self.rect = pg.Rect(posx, posy, image_width, image_length)

        # contains the descriptions of the player's images' directories
        self.action_array = ['idle', 'walk',  'damage']

        super().__init__(self.rect, image_width, image_length, self.action_array)
        
        self.physics = Physics(self, level)
        self.counter = Counter(screen, self, level)

    def run(self):
        '''Start the character's main functions'''

        if self.visible:
            # Display player
            self.screen.blit(self.image, self.rect)

        # Update the animation
        self.update_sprite()

        # Start the player's physics laws
        self.physics.run()

        # check all collisions against player
        self.physics.collision_check()

        # check if the cat goes out of the screen's range
        self.physics.range_reached()

    def won(self):
        # prevent player from being displayed after winning
        self.visible = False

    def lost(self):
        # prevent player from being displayed after winning
        self.visible = False

    def restart(self):
        '''move character back to starting position'''

        # to prevent player from restarting with a big gravity increase
        self.physics.gravity = 0

        self.rect.x = self.initial_posx
        self.rect.y = self.initial_posy
        
        self.visible = True
        self.update_current_sprite('idle')
