
import pygame as pg
import os

class Sprite(pg.sprite.Sprite):
    '''Manages sprite animation and image file paths. It also organizes the sprite images in 
        their correspondig array, based on their animation.
        The rect argument is used for the movement and position of the sprite animation'''

    def __init__(self, rect, image_width, image_length, action_array):
        pg.sprite.Sprite.__init__(self)

        self.image = None
        self.image_width = image_width
        self.image_length = image_length
        self.rect = rect
        self.frame_rate = 0.2
        self.update_spr = True
        self.current_sprite = 0

        # Will be used to create arrays that contain organized sprite images
        self.action_array = action_array     # contains the animation descriptions
        
        # Obtain the images' file directories 
        self.image_paths_dict = self.retrieve_file_paths(action_array)
        
        self.sprite_images_dict = dict()
        self.current_sprite_array = []
        
        # Create and assign images, organized based on action
        self.initialize_sprite_dict()

        self.mask = pg.mask.from_surface(self.image)

    def retrieve_file_paths(self, action_array):
        '''Obtains the directories of each image in the media file.
            Organizes each path in an array and then saves the arrays in
            a dict based on action descriptions in action_array'''
        
        media_directory = 'media/'
        paths = os.listdir(media_directory)

        self.sprites_file_paths = dict()

        for action in action_array: self.sprites_file_paths[action] = []

        # Obtain and assign the image directories
        for action, array in self.sprites_file_paths.items():

            for path in paths:
                if action in path:
                    array.append(''.join([media_directory, path]))
                    
                    # sort the path array starting from the first item
                    self.sort_paths(0)

        return self.sprites_file_paths

    # Chapter 6: Recursion
    def sort_paths(self, current_index):
        '''takes current index to use on the action array to keep track of the dict keys
            The arrays in the dict are accessed individually to sort in ascending order'''
        
        # case: stop the recursion once all elements in action_array have been accessed
        if current_index == len(self.action_array):
            return

        self.sprites_file_paths[self.action_array[current_index]].sort()

        self.sort_paths(current_index + 1)

    def initialize_sprite_dict(self):
        '''Assigns arrays containing sprite images to the sprite_images_dict
            based on image_paths_dict'''

        self.temp_array = []

        for sprite_paths_name, sprite_paths_array in self.image_paths_dict.items():
            for file_path in sprite_paths_array:

                self.set_file_path_name(file_path)

                self.set_surface_image()

                self.temp_array.append(self.image)

                # assign image array to the dict
            self.sprite_images_dict[sprite_paths_name] = self.temp_array.copy() 
            self.temp_array.clear()
        
        # set first sprite animation
        self.update_current_sprite(self.action_array[0]) 

    def set_file_path_name(self, name):
        self.file_name = name

        # create surface using current file_name
    def set_surface_image(self):
        self.image = pg.image.load(self.file_name).convert_alpha()
        self.resize_image()

    def resize_image(self):
        self.image = pg.transform.smoothscale(self.image, (self.image_width, self.image_length))

    def update_sprite(self): 
        '''Updates the sprite images to create animation'''

        # check if sprite animation is required
        if self.update_spr:
            if self.current_sprite < len(self.current_sprite_array) - 1:
                self.current_sprite += self.frame_rate
            else:
                self.current_sprite = 0

                # update current displayed frame
        self.image = self.current_sprite_array[int(self.current_sprite)]
        self.mask = pg.mask.from_surface(self.image)
    
    def update_current_sprite(self, action):
        '''Change the current animation'''
        
        self.current_sprite = 0

        # update the animation according to the passed action value
        if action in self.action_array:
            self.current_sprite_array = self.sprite_images_dict[action]
