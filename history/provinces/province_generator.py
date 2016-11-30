#!/usr/bin/python
# -*- coding: utf-8 -*-

for x in range(0, 543):
    letter = (x%26) + 65
    out = "%d - " % (x+1)
    if x > 25:
        out += chr((x//26) + 64)
    out += chr(letter)
    f = open(out + ".txt", "w")
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

discovered_by = chinese""".format(out, out.split(" - ")[1])
	)
f.close()
	
