import sys
from PIL import Image

def check(minOrMax, count, start):

	if minOrMax == "min":
		return count < start
	else:
		return count > start

def findExtreme(myImage, minOrMax, xOrY):

	xSize = myImage.size[0]
	ySize = myImage.size[1]

	if xOrY == "x":
		outside = xSize
		inside = ySize
	elif xOrY == "y":
		outside = ySize
		inside = xSize
	else:
		sys.exit("Input can only be either x or y.")

	if minOrMax == "min":
		start = outside - 1
		end = 0
	elif minOrMax == "max":
		start = 0
		end = outside - 1
	else:
		sys.exit("Input can only be either min or max.")

	# Find the smallest x-value
	myVal = start

	for row in range(inside):
		count = end

		if xOrY == "x":
			test = myImage.getpixel((count, row))
		else:
			test = myImage.getpixel((row, count))

		while test == 255 and check(minOrMax, count, start):
			
			if minOrMax == "min":
				count += 1
			else:
				count -= 1
			
			if xOrY == "x":
				test = myImage.getpixel((count, row))
			else:
				test = myImage.getpixel((row, count))
		
		if minOrMax == "min":
			if count < myVal:
				myVal = count
		else:
			if count > myVal:
				myVal = count

	return myVal

# Scales the image down to the default size
def scaleImage(myImage, width, height):

	xMin = findExtreme(myImage, "min", "x")
	xMax = findExtreme(myImage, "max", "x")
	yMin = findExtreme(myImage, "min", "y")
	yMax = findExtreme(myImage, "max", "y")

	myImage = myImage.crop((xMin, yMin, xMax+1, yMax+1))

	# Resizes the image to the given width x height
	myImage = myImage.resize((width,height))

	# Returns the scaled image
	return myImage