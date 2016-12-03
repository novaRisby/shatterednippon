from PIL import Image

prov_im = Image.open("provinces.bmp")
sea_im = Image.open("seatiles.bmp")
colors = []
sea_tiles = []

image_size = prov_im.size

for x in range(0, image_size[0]):
	for y in range(0, image_size[1]):
		cord = (x,y)
		pixel = prov_im.getpixel(cord)
		if pixel not in colors and not (pixel[0:3] == (255,255,255) or pixel[0:3] == (0,0,0)): # excluding pure white and black
			colors.append(pixel)

count = len(colors)

for x in range(0, image_size[0]): #
	for y in range(0, image_size[1]):
		cord = (x,y)
		pixel = sea_im.getpixel(cord)
		if pixel not in sea_tiles and pixel not in colors and not (pixel[0:3] == (255,255,255) or pixel[0:3] == (0,0,0)):
			sea_tiles.append(pixel)
			count += 1

with open("definition.csv", "w") as f:
	f.write("province;red;green;blue;x;x\n")
	count = 0
	for color in colors:
		count += 1
		f.write("%d;%s;%s;%s;%d;x\n" % (count, color[0], color[1], color[2], count+100))
	for tile in sea_tiles:
		count += 1
		f.write("%d;%s;%s;%s;%d;x\n" % (count, tile[0], tile[1], tile[2], count+1000))
