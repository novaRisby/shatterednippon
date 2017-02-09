#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import time

from PIL import Image

"""
As one can imagine, this script requires pillow to be installed.

The script is rather slow (takes about one minute to run on a standard EU4 map size), but since this script should only be run once per project I feel that this is an acceptable sacrifice. I've done what I can to optimise it.
"""

colors = []

def floodfill(image, x_start, y_start, fill_color):
    """
    Just your average floodfill algorithm.
    """
    pixel = image.load()
    xsize, ysize = image.size
    
    stack = set()
    stack.add((x_start, y_start))
    selection = set()
    try:
        orig_color = pixel[x_start, y_start]
        if orig_color == fill_color:
            return [] # seed point is already not matched
        selection.add((x_start, y_start))
    except IndexError:
        return [] # seed point outside image

    count = 0
    tid = time.clock()
    while stack:
        x, y = stack.pop()
        count += 1
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
        
def color_province(image, provinces, lower_range, higher_range):
    """Colors provinces with a random color in a given interval of RGB values. No duplicates."""
    pixel = image.load()
    rand = random.randint(lower_range[2], higher_range[2])
    rand_color = randomise_color(lower_range, higher_range)
    
    for province in provinces:
        count = 0
        while rand_color in colors:
            if count == 5000: # Sanity check to ensure the program does not run forever.
                sys.exit("Cannot find a unique color, either you are incredibly unlucky or the color interval is too close.")
            rand_color = randomise_color(lower_range, higher_range)
            count += 1
            
        floodfill(image, province[0][0], province[0][1], rand_color)
        colors.append(rand_color)

def randomise_color(lower_range, higher_range):
    return (random.randint(lower_range[0], higher_range[0]), random.randint(lower_range[1], higher_range[1]), random.randint(lower_range[2], higher_range[2]))
    
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

        
if __name__ == "__main__":
    t = time.clock()
          
    map_dir = os.getcwd()+"\\shatterednippon\\map\\"
    
    if os.path.isfile(map_dir+"provinces.bmp"):
        sys.exit("A \"provinces.bmp\" already exists. Please check if you want to keep this file.")
    
    land_color = (164, 164, 164)
    sea_color = (42, 42, 42)
    border_color = (0, 0, 0)
    fill_color = (255, 255 ,255) # Just a color that is different from the others
        
    land_tiles = []
    sea_tiles = []
    borders = []

    map_file = Image.open("map test.bmp")
    image_size = map_file.size
    print("size: ", image_size)
    pixel = map_file.load()
    
    for x in range(0, image_size[0]):
        for y in range(0, image_size[1]):
            pixel_color = pixel[x, y] # Gets the color of pixel at cord
            if pixel_color == land_color:
                land_tiles.append(floodfill(map_file, x, y, fill_color))
            elif pixel_color == sea_color:
                sea_tiles.append(floodfill(map_file, x, y, fill_color))
            elif pixel_color == border_color:
                borders.append((x, y))
            
    
    print ("time: ", time.clock() - t)
    t = time.clock()
    color_province(map_file, land_tiles, (10, 10, 0), (255, 255, 0))
    color_province(map_file, sea_tiles, (10, 200, 200), (125, 255, 255))
    color_in_borders_with_adjacent(map_file, borders)
    print ("coloring: ", time.clock() - t)
    
    map_file.show()
    
    print ("land_tiles: ", len(land_tiles))
    print ("sea_tiles: ", len(sea_tiles))