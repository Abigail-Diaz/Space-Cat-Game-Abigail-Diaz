#!/usr/bin/env python3

import pygame as pg
import sys
from Player import Player
from Platform import Level, screen_width, screen_length
from Shoot import Shoot
from Levels import *
from Sound import Sound
from Menu import Menu

def main():

    pg.init()

    # Set window display
    screen = pg.display.set_mode((screen_width, screen_length))
    pg.display.set_caption('Space Cat')

    # game feautures objects
    sound = Sound()
    menu = Menu(screen)
    level = Level(screen)
    cat = Player(120, 281,  60, 40, level, screen)

    # start running the game
    run_game(cat, level, sound, menu, screen)

def run_game(cat, level, sound, menu, screen):
    '''starts the game loop to keep the game running'''
    
    clock = pg.time.Clock()
    running = True
    fps = 60

    # for cat's shooting action
    shoot = Shoot(90, 90, cat, level.enemies, screen)

    sound.play_background_music()

    while running:
    
        for event in pg.event.get():
            if event.type ==  pg.QUIT:
                pg.quit()
                sys.exit()
    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    cat.physics.make_jump()
        
            if event.type ==  pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    cat.update_current_sprite('walk')
                    cat.physics.move_right(True)
                    cat.physics.move_left(False)
    
                if event.key == pg.K_LEFT:
                    cat.update_current_sprite('walk')
                    cat.physics.move_right(False)
                    cat.physics.move_left(True)

                if event.key == pg.K_x:
                    shoot.attack()

            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                    cat.update_current_sprite('idle')
                    cat.physics.move_right(False)
                    cat.physics.move_left(False)
        
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_click_pos = pg.mouse.get_pos()
                    if menu.start_text_rect.collidepoint(mouse_click_pos):
                        cat.counter.menu.start = False
                    if cat.counter.menu.restart_rect.collidepoint(mouse_click_pos):
                        # once restart button is clicked, restart the game
                        cat.restart()
                        cat.counter.restart()
                        level.restart()
                        shoot.restart()
        
        # keep object active and updated
        level.run()
        cat.counter.run() 
        cat.run()
        shoot.run()

        # start menu
        cat.counter.menu.start_menu()
        
        pg.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()