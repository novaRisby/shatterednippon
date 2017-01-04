#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Replaces any old version of the mod existing with the current directories' version.

Simply double click this file with Python installed to run the mod.
"""

import os
import shutil
import subprocess

mod = "shatterednippon"
mod_dir = os.getcwd()
eu4_mod_folder = "C:\\Users\\John\\Documents\\Paradox Interactive\\Europa Universalis IV\\mod\\"
eu4_game = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\"

if os.path.isdir(eu4_mod_folder+"\\"+mod+"\\"):
	shutil.rmtree(eu4_mod_folder+"\\"+mod+"\\")
for file in os.listdir(eu4_mod_folder):
	if file == mod+".mod":
		os.remove(eu4_mod_folder+file)
		break

shutil.copytree(mod_dir+"\\"+mod+"\\", eu4_mod_folder+"\\"+mod+"\\")
shutil.copy(mod_dir+"\\"+mod+".mod", eu4_mod_folder)

subprocess.call(eu4_game+"eu4.exe -debug")