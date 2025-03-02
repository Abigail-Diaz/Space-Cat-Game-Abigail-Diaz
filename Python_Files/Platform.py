
import pygame as pg
from Levels import level_map
from Enemy import Enemy
from Flag import Flag
import random

tile_size = 60
screen_width, screen_length = 850, tile_size * len(level_map)

class Tile (pg.sprite.Sprite):
    '''For tile creation and tile movement'''
    
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    def get_tile_position(self):
        return (self.rect.x, self.rect.y)
    
    def get_tile_rect(self):
        return self.rect
    
    def update(self, x_shift):
        self.rect.x += x_shift

class Level:
    '''Sets up the level using the Tile objects. Manages enemy object group 
        and level layout left-shifting as the player moves forward'''
    
    def __init__(self, surface):
        self.surface = surface

        self.tiles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.flags = pg.sprite.Group()

        self.setup_level(level_map)
        self.background = pg.image.load('media/Galaxy12.jpg').convert()
        self.background = pg.transform.smoothscale(self.background, (screen_width, screen_length))
        self.shift = 0
        self.distance_traveled = 0
        self.enemy_speed = -3
        self.enemy_respawn_rate = 40

        self.enemy_collision_rect = pg.Rect(0, 0, 10, 10)
        self.tile_collision_rect = pg.Rect(0, 0, 10, 10)
        
    def setup_level(self, layout):
        '''Creates the tile layout/map, including some enemies and the flag, based on the given level map'''
        
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if col == 'F':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    flag = Flag(x, y, 100, 100)
                    self.flags.add(flag)
                if col == 'E':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    enemy = Enemy(x, y, 50, 50)
                    self.enemies.add(enemy)

    def run(self):
        '''Updates the flags and enemies constant actions. Displays the map layout and background  on the screen'''
        
        self.enemies.update(self.enemy_speed) 
        self.flags.update()
        self.surface.blit(self.background, (0, 0))
        
        self.flags.draw(self.surface)
        self.tiles.draw(self.surface)
        self.enemies.draw(self.surface)
        
        # new enemy objects created once enemies are off the screen
        self.respawn()
    
    def get_tile_collision_rect(self, player):
        '''Returns the tile rect the passed player object collided with'''
        
        for tile in self.tiles:
            if tile.rect.colliderect(player.rect):
                self.tile_collision_rect = tile.get_tile_rect()
                return self.tile_collision_rect
    
    def get_enemy_collision_rect(self, player):
        '''Returns the enemy rect the passed player object collided with'''
        
        for enemy in self.enemies:
            if enemy.rect.colliderect(player.rect):
                self.enemy_collision_rect = enemy.get_enemy_rect()
                return self.enemy_collision_rect

    def move_screen_forward(self, x_shift):
        '''Shifts the whole tile layout to the left'''
        
        self.distance_traveled += abs(x_shift)
        self.tiles.update(x_shift)
        self.flags.update(x_shift)
    
    def respawn(self):
        '''Adds new enemy objects with random starting postions once previous onces are out of the screen'''
        
        if len(self.enemies) > 1:
            self.list_of_alive_sprites = self.enemies.sprites()

            # check if enemy sprite is out of range
            for sprite in self.list_of_alive_sprites:
                if sprite.rect.x < 0:
                    # clean up the group from out of range enemies
                    self.enemies.remove(sprite)
        else:
            for num in range(self.enemy_respawn_rate):
                randy = random.randint(1, 800)
                randx = random.randint(800, 2000)
                enemy = Enemy(randx, randy, 50, 50)
                self.enemies.add(enemy)
    
    def change_enemy_speed(self, speed):
        self.enemy_speed = speed

    def restart(self):
        '''Sets the level tiles to original position'''

        # subtract distance traveled from current level position
        self.move_screen_forward(self.distance_traveled)
        self.distance_traveled = 0

        self.enemies.empty()
    

        
