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
tradegoods.bmp		   	- an image painted with correct tradegoods RGB values
provinces.bmp			- an image that defines provinces
00_tradegoods.txt		- defines tradegoods
definition.csv			- defines provinces
[province number - province_name].txt - the actual province file in the directory \history\provinces\
"""

def find_terrain(filepath):
    return None

def get_defined_terrains():
    names = []
    colors = []
    with open(os.getcwd()+"/shatterednippon/map/terrain.txt", "r") as f:
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
    names, colors = get_defined_terrains()
    print(names)
    print(colors)
