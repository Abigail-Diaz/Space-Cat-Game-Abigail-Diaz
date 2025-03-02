from Sprites import Sprite
import pygame as pg

class Flag(Sprite):
    '''To create rect object with flag animation and handle position'''
    def __init__(self, posx, posy, image_width, image_length):
        self.flag_width = 50
        self.flag_height = 50
        self.rect = pg.Rect(posx, posy, image_width, image_length)
        self.action_array = ['flag']
        super().__init__(self.rect, image_width, image_length, self.action_array)
    
    def update(self, update = 0):
        self.update_sprite()
        self.rect.x += update