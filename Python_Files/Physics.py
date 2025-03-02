
import pygame as pg

class Physics:
    '''Manages player's movements and checks for collisions'''
    def __init__(self, player, level):
        self.player = player
        self.rect = player.rect
        self.level = level
        self.jump = False
        self.fall = True
        self.gravity = 0
        self.left_axis_movement = False
        self.velocity = 0
        self.direction = {"right": False, "left": False}
        self.current_direction = None
        self.flag_collision = False
        self.on_floor_counter = 0
        self.non_col = 0
        self.collision_rect = pg.Rect(0, 0, 10, 10)
    
    def run(self):
        '''check player's actions'''
        self.horizontal_movement()
        self.jumping()
        self.falling()
    
    def horizontal_movement(self):
        '''Moves player left or right'''
        if self.direction['right'] and self.player.rect.x < 300:
            self.rect.x += 3
            
        if self.direction['left']:
            self.rect.x -= 3

    def jumping(self):
        # Character will move on the x axis as it completes the jump
        if self.jump:
            self.fall = True 

            if self.direction['left']:
                self.rect.x -= 2

    def falling(self):
        # Character will fall down as y value of rect increase
        if self.fall:
            self.gravity += 1
            self.rect.y += self.gravity 
    
    def make_jump(self):
        self.jump = True

        # gravity will allow the character to gradually go up, 
        # mimicking a jump
        self.gravity = -15

    def stop_jump(self):
        self.jump = False
    
    def make_fall(self):
        self.fall = True
    
    def stop_fall(self):
        self.fall = False

    def move_right(self, bool):
        '''Takes a booolean value to make the player walk right or not'''
        self.direction['right'] = bool
    
    def move_left(self, bool):
        '''Takes a booolean value to make the player walk left or not'''
        self.direction['left'] = bool
    
    def floor_reached(self, floor):
        '''Keep player on the floor'''

            # prevent player from falling through the tiles
        if self.rect.bottom >= floor: 
            self.rect.bottom = floor
            self.jump = False                                                                                                  
    
    def range_reached(self):
        '''Reset cat position to the the start (left) of the screen if it goes out of the screen's range'''
        if self.rect.left < 0:  
            self.rect.x = 25
        
        # prevent player from going off screen when jumping
        if self.rect.top < 0:
            self.rect.top = 0
    
    def repel_to_left(self):
        '''Repel player to the left by decreasing x value '''
        self.rect.x -= 5

    def repel_to_right(self):
        '''Repel player to the right by increasing x value'''
        self.rect.x += 5

    def repel_down(self):
        '''Repel player down by increasing its y value'''
        self.rect.y += 10
        self.fall = True

    def collision_check(self):
        '''Checks all collisions between player and enemy, flag and tiles'''

        self.check_tile_collision()
        self.check_flag_collision()
        self.check_enemy_collision()

    def check_tile_collision(self):
        '''Handles player's behavior when colliding with a tile'''

        left_collision = False

        collision = pg.sprite.spritecollide(self.player, self.level.tiles, False, pg.sprite.collide_mask)

        if self.direction['right'] and self.player.rect.x >= 300 and left_collision == False:
            self.level.move_screen_forward(-2) 

        if collision:
            self.gravity = 0
            self.non_col = 0
            self.fall = False
            self.jump = False                                                                                          
            
            self.collision_rect = self.level.get_tile_collision_rect(self.player)

            if self.collision_rect != None:
            
                # Upon collision, check if player is on top of a tile
                if  ((self.player.rect.left < self.collision_rect.right or self.player.rect.right > self.collision_rect.left) and ((abs(self.rect.bottom - self.collision_rect.top) < 50))):
                    self.on_floor_counter += 1
            
                    if (abs(self.rect.bottom - self.collision_rect.top)) < 50:
                        self.rect.bottom = self.collision_rect.top + 0.5

                # check if collision is with the bottom of a tile
                elif  ((self.rect.left < self.collision_rect.right or self.rect.right > self.collision_rect.left) and (abs(self.rect.top - self.collision_rect.bottom) < 20)):
                    self.repel_down()
            
                # check if collision is from the left of a tile
                elif self.collision_rect.right > self.rect.right and (self.rect.bottom > self.collision_rect.top):
                    self.fall = False
                    self.on_floor_counter = 0
                    self.repel_to_left()
                    left_collision = True

                # check if collision is from the right of a tile
                elif self.collision_rect.left < self.rect.left and (self.rect.bottom > self.collision_rect.top):
                    self.repel_to_right()
                    self.on_floor_counter = 0
                    self.fall = False

        else:
            # prevents unintended fall value from becoming true when else becomes true for a moment
            # to avoid alternation between else and floor collision, so fall does not become true while being on the floor
            if self.non_col > 4: 
                self.fall = True
            self.non_col += 1

    def check_flag_collision(self):
        '''Check if player collides with the flag object. 
            if collision happens, player wins and the win menu is called'''
        if self.player.visible:
            self.flag_collision = pg.sprite.spritecollide(self.player, self.level.flags, False, pg.sprite.collide_mask)
        
        if self.flag_collision:
            self.player.counter.menu.won_menu()
            self.player.won()

    def check_enemy_collision(self):
        '''Keeps track of collision between enemy and player object.
            Updates health bar when player sustains damage after colliding with an enemy'''
        
        enemy_collision = pg.sprite.spritecollide(self.player, self.level.enemies, False, pg.sprite.collide_mask)
        enemy_rect_collision = self.level.get_enemy_collision_rect(self.player)
        
        if enemy_collision and self.player.visible:
            self.player.update_current_sprite('damage')
            
            if self.rect.x < enemy_rect_collision.x:
                
                # repel player to the left, away from enemy object
                self.rect.x -= 20

            elif self.rect.x > enemy_rect_collision.x:

                # repel player to the right, away from enemy object
                self.rect.x += 20

                # count the collision against the health bar
            self.player.counter.collision()
        