#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image

import os
import codecs

if ("scripts" in os.getcwd()):
    cwd = os.getcwd().replace("\\scripts", "")
else:    
    cwd = os.getcwd()
print(cwd)
prov_dir = cwd+"\\shatterednippon\\history\\provinces\\"
local_dir = cwd+"\\shatterednippon\\localisation\\"
map_dir = cwd+"\\shatterednippon\\map\\"

local_file = open(local_dir + "prov_names_l_english.yml", "w")
local_file.write("l_english:\n")

definitions = open(map_dir + "definition.csv", "w")
definitions.write("province;red;green;blue;x;x\n")

im = Image.open(map_dir+"provinces.bmp")
colors = []

image_size = im.size
pixel = im.load()

land_tiles = 0
sea_tiles = 0
"""
for y in range (image_size[1]):
    for x in range (image_size[0]):
        pixel_color = pixel[x, y]
        if pixel_color not in colors and not (pixel_color == (255,255,255) or pixel_color == (0,0,0)): # excluding pure white and black
            colors.append(pixel)
            if pixel_color[2] > 0:
                sea_tiles += 1
            else:
                land_tiles += 1

"""
colors = im.getcolors(maxcolors=10000) # Arbitrary maxcolors number
for color in colors:
    color = color[1]
    if color[2] > 0:
        sea_tiles += 1
    else:
        land_tiles += 1

print("land: ", land_tiles)
print("sea: ", sea_tiles)
provinces = len(colors)

x = 0
for color in colors:
    color = color[1]
    if color[2] == 0:
        out = "%d - PROV%d" % (x+1, x+1)
        """
            letter = (x%26) + 65
            out = "%d - " % (x+1)
            if x > 25:
                out += chr((x//26) + 64)
            out += chr(letter)
        """
        if (x < land_tiles):
            f = open(prov_dir + out + ".txt", "w")
            f.write	(
"""# {0}

owner = JAP
add_core = JAP
controller = JAP

is_city = yes
hre = no

religion = shinto
culture = japanese

base_tax = 2
base_production = 2
base_manpower = 2

trade_goods = silk

capital = "{1}"

discovered_by = chinese""".format(out, out.split(" - ")[1]))
        local_file.write(' PROV{0}:0 "{1}"\n'.format(x+1, out.split(" - ")[1]))
        
        definitions.write("{0};{1};{2};{3};;{4}\n".format(x+1, color[0], color[1], color[2], out.split(" - ")[1]))
        
        #definitions.write("{0};{1};{2};{3};;{4}\n".format(x+1, color[1][0], color[1][1], color[1][2], out.split(" - ")[1]))
        
        f.close()

        x += 1

local_file.close()
definitions.close()

print (str(x) + " provinces defined.")
