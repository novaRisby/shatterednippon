#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import fileinput
from PIL import Image

"""
Requires:
A folder structure according to Paradox's own: [cwd]\history\provinces\
Files:
terrain.bmp             - an image painted with correct terrain RGB values
provinces.bmp           - an image that defines provinces
terrain.txt             - defines terrains
definition.csv          - defines provinces
[province number - province_name].txt - the actual province file in the directory \history\provinces\
"""

def override_terrain(path, prov_num, terrain_type):
    

def get_province_number(path, corr_pixel):
    """
    Checks definition.csv if provinces.bmp's corresponding pixel's RBG value is in the definition list. Returns the province number if it finds the pixel in the list, returns None otherwise.
    """
    corr_pixel = str(corr_pixel).strip("()").replace(", ", ";") #Reformats the pixel to ensure it can be compared.
    with open(path + "\\map\\definition.csv", "r") as definitions:
        prov_num = 1
        for line in definitions:
            if corr_pixel in line:
                return prov_num
            prov_num += 1
    return None    
    
def get_defined_terrains(path):
    names = []
    colors = []
    with open(path+terrain.txt", "r") as f:
        for line in f:
            if re.match("\t\w+ = {", line):
                names.append(line.strip("={} \n\t"))
                terrain = True
                count = 0
            elif re.match("\s*color.*{\s*\d+\s*\d+\s*\d+\s*}", line):
                numbers = tuple(map(int, re.sub("[^\d. ]\s*", "", line).split()))
                colors.append(numbers)
            elif "\t}" in line:
                try:
                    if colors[count] is not None:
                        pass
                except IndexError:
                    colors.append([])
                    terrain = False
                count += 1
        return names, colors

            

if __name__ == "__main__":
    im = Image.open("terrain.bmp")
    path = os.getcwd()+os.pardir()+"\\shatterednippon\\map\\"
    prov_im = Image.open(path + "map\\provinces.bmp")

    names, colors = get_defined_terrains(path)
    pixel = im.load()
    prov_pixel = prov_im.load()
    
    checked = [] #A list of checked corresponding RGB colors.

    for y in range(im.size[1])
        for x in range(im.size[0])
            pixel_color = pixel[x, y]
            prov_pixel_color = prov_pixel[x, y]
            if prov_pixel_color not in checked and pixel_color in colors:
                checked.append(prov_pixel_color)
                prov_num = get_province_number(path, prov_pixel_color)
                if prov_num:
                    override_terrain(path, prov_num, names[colors.index(pixel_color)])
            
    print(names)
    print(colors)
