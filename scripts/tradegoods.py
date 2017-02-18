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

def replace_tradegood(prov_num, new_tradegood):
	"""
	Replaces the given province's tradegood with the new one defined in the tradegoods.bmp map.
	"""
	directory = os.getcwd()+"\\shatterednippon\\history\\provinces\\"
	for file in os.listdir(directory):
		if file.startswith(str(prov_num)):
			old_tradegood = find_tradegood(directory+file)
			if old_tradegood is None:
				print("Province: %s has no \"trade_goods\" variable" % file)
				return
			elif new_tradegood == old_tradegood:
				return
			
			for line in fileinput.input(directory+file, inplace=True):
				line = line.rstrip().replace(old_tradegood, new_tradegood)
				print(line)
			print("Province %d: changed tradegood from %s to %s" % (prov_num, old_tradegood, new_tradegood))
			return

def find_tradegood(filepath):
	"""
	Finds the given province file's tradegood and returns it, else returns None.
	"""
	with open(filepath) as f:
		for line in f:
			if "trade_good" in line:
				return line.replace("trade_goods = ", "").strip()
		return None
	
def get_province_number(corr_pixel):
	"""
	Checks definition.csv if provinces.bmp's corresponding pixel's RBG value is in the definition list. Returns the province number if it finds the pixel in the list, returns None otherwise.
	"""
	corr_pixel = str(corr_pixel).strip("()").replace(", ", ";") #Reformats the pixel to ensure it can be compared.
	with open(os.getcwd()+"\\shatterednippon\\map\\definition.csv", "r") as definitions:
		prov_num = 1
		for line in definitions:
			if corr_pixel in line:
				return prov_num
			prov_num += 1
	return None
	
def get_defined_tradegoods():
	"""
	Returns the names of the tradegoods and the RGB color values for each defined tradegood in 00_tradegoods.txt as two seperate lists.
	"""
	names = []
	colors = []
	with open(os.getcwd()+"\\shatterednippon\\common\\tradegoods\\00_tradegoods.txt", "r") as f:
		for line in f:
			if line[0].isalpha():
				names.append(line.strip("={} \n"))
			elif "color" in line:
				numbers = tuple(map(int, re.sub("[^\d. ]\s*", "", line).split()))
				colors.append(tuple(round(i * 255) for i in numbers))
		return names, colors

if __name__ == '__main__':
	im = Image.open("tradegoods.bmp")
	prov_im = Image.open(os.getcwd()+"\\shatterednippon\\map\\provinces.bmp")
	image_size = im.size

	names, colors = get_defined_tradegoods()
	checked = [] #A list of checked corresponding RGB colors.
	for x in range(0, image_size[0]):
		for y in range(0, image_size[1]):
			cord = (x, y)
			pixel = im.getpixel(cord)
			corr_pixel = prov_im.getpixel(cord)

			if corr_pixel not in checked and pixel in colors:
				checked.append(corr_pixel)
				prov_num = get_province_number(corr_pixel)
				if prov_num:
					replace_tradegood(prov_num, names[colors.index(pixel)]) # tradegood name of a given RGB tuple
		
