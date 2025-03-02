from Platform import screen_width, screen_length

import pygame as pg

class Menu:
    '''Creates the menus for winning, loosing and starting the game'''
    def __init__(self, screen):
        self.start = True
        self.screen = screen
        
        green = (0, 255, 0)
        blue = (0, 0, 128)
        purple = (128, 0, 128)
        white = (255, 255, 255)
        self.font = pg.font.Font('freesansbold.ttf', 32)
        
        self.blue_square_width = 300
        self.blue_square_height = 300
        self.blue_square_posx = screen_width/2 - 150
        self.blue_square_posy = screen_length/3
        
        self.restart = pg.image.load('media/restart.png').convert_alpha()
        self.restart = pg.transform.smoothscale(self.restart, (self.blue_square_width/2, 50))
        self.restart_rect = self.restart.get_rect()
        
        self.start_text = self.font.render('Start', True, green, blue)
        self.start_text_rect = self.start_text.get_rect()
        
        self.loose_text = self.font.render('You lose!', True, green, blue)
        self.loose_text_rect = self.loose_text.get_rect()

        self.win_text = self.font.render('You won!', True, purple, white)
        self.win_text_rect = self.win_text.get_rect()

        self.blue_square = pg.Surface((self.blue_square_width, self.blue_square_height))
        self.blue_square.fill('blue')
        
        self.restart_posx = self.blue_square_posx + self.blue_square_width/4
        self.restart_posy = self.blue_square_posy + self.blue_square_height/2
        self.restart_rect.x = self.restart_posx
        self.restart_rect.y = self.restart_posy

        self.start_text_rect.centerx = self.blue_square_posx + self.blue_square_width/2
        self.start_text_rect.y = self.restart_posy
        
        self.loose_text_rect.centerx = self.blue_square_posx + self.blue_square_width/2
        self.loose_text_rect.centery  = self.blue_square_posy + self.blue_square_width/4

        self.win_text_rect.centerx = self.blue_square_posx + self.blue_square_width/2
        self.win_text_rect.centery = self.blue_square_posy + self.blue_square_width/4

    def start_menu(self):
        if self.start:
            self.screen.blit(self.blue_square, (self.blue_square_posx, self.blue_square_posy))
            self.screen.blit(self.start_text, self.start_text_rect)
    
    def restart_menu(self): 
        self.screen.blit(self.blue_square, (self.blue_square_posx, self.blue_square_posy))
        self.screen.blit(self.restart, self.restart_rect)
        self.screen.blit(self.loose_text, self.loose_text_rect)

    def won_menu(self):
        '''Menu announces player has won and allows for a restart'''
        self.screen.blit(self.blue_square, (self.blue_square_posx, self.blue_square_posy))
        self.screen.blit(self.restart, self.restart_rect)
        self.screen.blit(self.win_text, self.win_text_rect)
    
    