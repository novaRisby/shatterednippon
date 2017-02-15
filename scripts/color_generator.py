#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
#import time
#import _thread
#import pygame

from PIL import Image

"""
As one can imagine, this script requires pillow to be installed.

The script is rather slow (takes about one minute to run on a standard EU4 map size), but since this script should only be run once per project I feel that this is an acceptable sacrifice. I've done what I can to optimise it.
"""

def floodfill(image, x_start, y_start, fill_color, return_selection = False):
    """
    Just your average floodfill algorithm. Warning if return_selection is set to True and you try to fill something incredibly large your machine might run out of memory.
    """
    pixel = image.load()
    xsize, ysize = image.size
    
    try:
        orig_color = pixel[x_start, y_start]
        if orig_color == fill_color:
            return [] # seed point is already not matched
    except IndexError:
        return [] # seed point outside image
    
    stack = set()
    stack.add((x_start, y_start))
    
    if return_selection:
        selection = set()
        selection.add((x_start, y_start))

        while stack:
            x, y = stack.pop()
            if pixel[x, y] == orig_color:
                pixel[x, y] = fill_color
                selection.add((x, y))
                if x > 0:
                    stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))
        return list(selection)
        
    else:
        while stack:
            x, y = stack.pop()
            if pixel[x, y] == orig_color:
                pixel[x, y] = fill_color
                if x > 0:
                    stack.add((x - 1, y))
                if x < (xsize - 1):
                    stack.add((x + 1, y))
                if y > 0:
                    stack.add((x, y - 1))
                if y < (ysize - 1):
                    stack.add((x, y + 1))
        
def randomise_color(lower_range, higher_range, colors = None):
    count = 0
    while True:
        if count == 5000: # Sanity check to ensure the program does not run forever.
            sys.exit("Cannot find a unique color, either you are incredibly unlucky or the color interval is too close.")
        rand_color = (random.randint(lower_range[0], higher_range[0]), random.randint(lower_range[1], higher_range[1]), random.randint(lower_range[2], higher_range[2]))
        count += 1
        if rand_color not in colors:
            return rand_color
    
def color_in_borders_with_adjacent(image, borders):
    pixel = image.load()
    xsize, ysize = image.size
    
    orig_color = pixel[borders[0][0], borders[0][1]]
    
    for border in borders:
        x, y = border
        if x >= 0 and x <= (xsize - 1) and y >= 0 and y <= (ysize - 1):
            try:
                if orig_color != pixel[x, y-1]:
                    pixel[x, y] = pixel[x, y-1]
            except IndexError:
                pass
            try:
                if orig_color != pixel[x+1, y]:
                    pixel[x, y] = pixel[x+1, y]
            except IndexError:
                pass
            try:
                if orig_color != pixel[x-1, y]:
                    pixel[x, y] = pixel[x-1, y]
            except IndexError:
                pass
            try:
                if orig_color != pixel[x, y+1]:
                    pixel[x, y] = pixel[x, y+1]
            except IndexError:
                pass

        
def make_provinces_bmp(map_file): 
    land_color = (91, 91, 91)
    sea_color = (213, 213, 213)
    land_border_color = (255, 255, 255)
    sea_border_color = (0, 0, 0)
    
    #land_color = (164, 164, 164)
    #sea_color = (42, 42, 42)
    #land_border_color = (0, 0, 0)
    #sea_border_color = (255, 255, 255)
    
    land_tiles = []
    sea_tiles = []
    land_borders = []
    sea_borders = []
    
    colors = []

    image_size = map_file.size
    print("size: ", image_size)
    pixel = map_file.load()
    
    for y in range(image_size[1]):
        for x in range(image_size[0]):
            pixel_color = pixel[x, y] # Gets the color of pixel at cord
            if pixel_color == land_color:
                rand_color = randomise_color((10, 10, 0), (255, 255, 0), colors)
                land_tiles.append(floodfill(map_file, x, y, rand_color, True))
                colors.append(rand_color)
            elif pixel_color == sea_color:
                rand_color = randomise_color((10, 200, 200), (125, 255, 255), colors)
                sea_tiles.append(floodfill(map_file, x, y, rand_color, True))
                colors.append(rand_color)
            elif pixel_color == land_border_color:
                land_borders.append((x, y))
            elif pixel_color == sea_border_color:
                sea_borders.append((x, y))
            

    print("land_tiles: ", len(land_tiles))
    print("sea_tiles: ", len(sea_tiles))
    color_in_borders_with_adjacent(map_file, land_borders)
    color_in_borders_with_adjacent(map_file, sea_borders)
    
    
"""
def display(map_file):
    n=1
    pygame.init()
    size = map_file.size
    w, h = size
    size=(w,h)
    screen = pygame.display.set_mode(size) 
    c = pygame.time.Clock() # create a clock object for timing

    while True:
        img=pygame.image.load(filename) 
        screen.blit(img,(0,0))
        pygame.display.flip() # update the display
        c.tick(10) # only three images per second
"""

if __name__ == "__main__":
    map_dir = os.getcwd()+"\\shatterednippon\\map\\"
    """
    if os.path.isfile("provinces.bmp"):
        sys.exit("A \"provinces.bmp\" already exists. Please check if you want to keep this file.")
    """
    map_file = Image.open("provinces.bmp")
    """
    map_file = _thread.start_new_thread(make_provinces_bmp, (map_file,))
    display(map_file)
    """
    make_provinces_bmp(map_file)
    map_file.save("random.bmp")