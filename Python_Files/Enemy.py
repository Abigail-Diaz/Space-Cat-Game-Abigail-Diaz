from Sprites import Sprite
import pygame as pg

class Enemy(Sprite):
    '''For enemy object creation, sprite animaytion and position update'''

    def __init__(self, posx, posy, image_width, image_length):
        self.action_array = ['eye']
        self.rect = pg.Rect(posx, posy, image_width, image_length)
        super().__init__(self.rect, image_width, image_length, self.action_array)

    def update(self, x_shift):

        # update position of rect
        self.rect.x += x_shift

        # keep animation active
        self.update_sprite()

    def get_enemy_rect(self):
        return self.rect