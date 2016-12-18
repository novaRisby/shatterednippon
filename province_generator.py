#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

prov_dir = os.getcwd()+"\\shatterednippon\\history\\provinces\\"
local_dir = os.getcwd()+"\\shatterednippon\localisation\\"

local_file = open(local_dir + "prov_names_l_english.yml", "w")
local_file.write("l_english:\n")

land_tiles = 451
sea_tiles = 91
provinces = land_tiles + sea_tiles


for x in range(0, provinces):
	letter = (x%26) + 65
	out = "%d - " % (x+1)
	if x > 25:
		out += chr((x//26) + 64)
	out += chr(letter)
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
	f.close()
local_file.close()


