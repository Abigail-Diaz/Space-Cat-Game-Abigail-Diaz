
import pygame as pg
class Sound:
    '''Manges sound effect for shooting and background music'''
    
    def __init__(self):
        self.background_volume = 0.01
        self.shot_volume = 0.5

        # load music
        self.background_sound = pg.mixer.Sound('media/Battle in the Stars.ogg')
        self.background_sound.set_volume(self.background_volume)
        self.shot_sound = pg.mixer.Sound('media/shot.wav')
        self.shot_sound.set_volume(self.shot_volume)

    def play_background_music(self):
        pg.mixer.Channel(0).play(pg.mixer.Sound(self.background_sound), loops = -1)
    
    def play_shot_sound(self):
        pg.mixer.Channel(1).play(pg.mixer.Sound(self.shot_sound))