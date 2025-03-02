import pygame as pg

from Sprites import Sprite

class Fire(Sprite):
    '''For fire sprite creation and position update'''
    def __init__(self, image_width, image_length, shooting_obj):
        
        self.shooting_obj = shooting_obj
        self.posx, self.posy = shooting_obj.rect.center
        self.rect = pg.Rect(self.posx - 10, self.posy - 20, image_width, image_length)
        self.action_array = ['spark', 'hits']
        Sprite.__init__(self, self.rect, image_width, image_length, self.action_array)

    def update(self, option = '', x_shift = 2):
        '''Updates the fire's position, animation and change of animation'''
        
        self.rect.x += x_shift
        
        # keeps animation running
        self.update_sprite()
        
        if option == 'hits':
            self.update_current_sprite('hits')

    def get_fire_rect(self):
        return self.rect
        
