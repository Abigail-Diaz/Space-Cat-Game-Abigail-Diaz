import pygame as pg
from Fire import Fire
from Sound import Sound

class Shoot:
    '''Handles fire objects and player's attack'''
    def __init__(self, image_width, image_length, shooting_obj, damaged_obj, surface):
        self.image_width  = image_width
        self.image_length = image_length
        self.fire_size = 50
        self.running = False
        self.shooting = False
        self.surface = surface
        self.fire_sprite_group = pg.sprite.Group()
        self.fire = Fire(self.fire_size, self.fire_size, shooting_obj)
        self.shooting_obj = shooting_obj
        self.damaged_obj = damaged_obj
        self.collision_rect = None
        self.sound = Sound()

    def run(self):
        ''' Activate the fire sprite group display and sprite update'''
        self.fire_sprite_group.draw(self.surface)
        self.fire_sprite_group.update()
        self.shot()
        
    def attack(self):
        '''creates a new fire object once player shoots'''
        self.create_another_fire()
        self.sound.play_shot_sound()

    def create_another_fire(self):
        '''Creates a new fire object to be added to the existing fire sprite group'''
        new_fire = Fire(self.fire_size, self.fire_size, self.shooting_obj)
        self.fire_sprite_group.add(new_fire)

    def shot(self):
        '''checks if the passed object was hit by a fire object. If so, the fire group's animation is updated'''
        self.collision = pg.sprite.groupcollide(self.damaged_obj, self.fire_sprite_group, True, False)

        if self.collision:
            self.fire_sprite_group.update('hits')
        else:
            self.fire_sprite_group.update('spark')
    
    def restart(self):
        self.clear_fire_group()
    
    def clear_fire_group(self):
        self.fire_sprite_group.empty()