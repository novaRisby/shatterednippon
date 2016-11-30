from PIL import Image

im = Image.open("try.bmp")
colors = []

image_size = im.size

for x in range(0, image_size[0]):
	for y in range(0, image_size[1]):
		cord = (x,y)
		pixel = im.getpixel(cord)
		if pixel not in colors and not (pixel[0:3] == (255,255,255) or pixel[0:3] == (0,0,0)): # excluding pure white and black
			colors.append(pixel) 

with open("definition.csv", "w") as f:
	f.write("province;red;green;blue;x;x\n")
	count = 0
	for color in colors:
		count += 1
		f.write("%d;%s;%s;%s;%d;x\n" % (count, color[0], color[1], color[2], count+100))
