#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import time

from PIL import Image

map_dir = os.getcwd()+"\\shatterednippon\\map\\"

land_color = (164, 164, 164) # Green
water_color = (42, 42, 42) # Cyan
border_color = (0, 0, 0)
    
land_tiles = []
sea_tiles = []
borders = []
prov = []
provinces = []
checked_cords = []

map_file = Image.open("map.bmp")
image_size = map_file.size()
map_file.show()

def color_borders():
    pass

def floodfill(xsize, ysize, x_start, y_start, colorToMatch):
    # An implementation of the fast flood fill algorithm found in the article: 
    #https://www.codeproject.com/Articles/16405/Queue-Linear-Flood-Fill-A-Fast-Flood-Fill-Algorith
    pixels_checked = [(x_start, y_start)]
    color = map_file.getpixel(x_start, y_start)
    
    while pixels_checked:
        x, y = pixels_checked.pop(0)
        pixels_checked = pixels_checked[1:]
        
        color = map_file.getpixel(x, y)
        if color == colorToMatch:
            if x > 0:
                pixels_checked.append(x - 1, y)
            if x < (xsize - 1):
                pixels_checked.append(x + 1, y)
            if y > 0:
                pixels_checked.append(x, y - 1)
            if y < (ysize - 1):
                pixels_checked.append(x, y + 1)
    return pixels_checked
        
def color_province():
    for i in range(0, len(provinces)):
        if i % 2 == 0:
            return True
        
if __name__ == "__main__":
    t = time.clock()
    if os.isfile(map_dir+"provinces.bmp"):
        sys.exit()
    
    for x in range(0, image_size[0]):
        for y in range(0, image_size[1]):
            cord = (x,y)
            pixel_color = map_file.getpixel(cord) # Gets the color of pixel at cord
            if cord in checked_cords:
                continue
            
            if pixel_color != border_color:
                if pixel_color == land_color:
                    provinces.append(floodfill(image_size[0], image_size[1], x, y, land_color))
                elif pixel_color == water_color:
                    provinces.append(floodfill(image_size[0], image_size[1], x, y, water_color))
            else: # pixel_color == border_color
                borders.append(pixel_color)
    print (time.clock() - t)
    print (len(provinces))