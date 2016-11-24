import sys
import copy
from PIL import Image

#myImage = Image.open("testing2.jpg").convert("L")

myImage = Image.new("L", (90,90), color=255)

myImage.putpixel((40,45), 65)
myImage.putpixel((60,50), 65)

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

	print("xMin:", xMin, "xMax:", xMax)
	print("yMin:", yMin, "yMax:", yMax)

	myImage = myImage.crop((xMin, yMin, xMax+1, yMax+1))

	# Resizes the image to the given width x height
	myImage = myImage.resize((width,height))

	# Returns the scaled image
	return myImage

def imgArr(myImage):

	# Create array of image values
	imgArr = []

	# Get height and width values
	height = myImage.height
	width = myImage.width

	# Get all rows
	for i in range(height):
		row = []

		# Add each value to the row
		for j in range(width):
			row.append(myImage.getpixel((j,i)))

		# Append the row to the main array
		imgArr.append(row)

	return imgArr

# Input:
#	myImage: the padded image to apply the filter to
#	matrix: the matrix to use to multiply the image by
# Output:
#	Filtered image
def applyFilter(myImage, kernel):

	a = 0

	offset = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,0], [0,1], [1,-1], [1,0], [1,1]]

	for i in range(1, myImage.height-1):
		for j in range(1, myImage.width-1):

			for k in range(len(kernel)):
				a += (myImage.getpixel((j+offset[k][0],i+offset[k][1])) * kernel[k])

			myImage.putpixel((j,i), a)


	return myImage

def addPadding(im):
	filtered = Image.new("L", (im.width + 2, im.height + 2), color = 0) #create new image that is 2 pixels wider and taller than the original

	filtered.paste(im, (1, 1), None) #copy image into new image with padding of a 1 pixel border around

	return filtered

# Checks if a pixel is in the recorded array yet or not
def notRecorded(recorded, x, y):

	result = True

	# Check if the pixel to check matches a pixel in the recorded array
	# Recorded is a 2D array such that each entry contains a [x, y] array of pixels found
	for item in recorded:
		if item[0] == x and item[1] == y:
			result = False

	return result

# Recursive search to find the 
def pixelSearch(originalImage, newImage, recorded, curPixel):

	# Check if the current pixel is white. If so do nothing and return the newImage and recorded
	if originalImage.getpixel((curPixel[0], curPixel[1])) != 255 and notRecorded(recorded, curPixel[0], curPixel[1]):

		# Add the current pixel in the same location to the new image
		newImage.putpixel((curPixel[0], curPixel[1]), originalImage.getpixel((curPixel[0], curPixel[1])))
		# Add the current pixel to the recorded array
		recorded.append(copy.deepcopy(curPixel))

		# Search the four pixels (below or right)
		# Decision structure to handle edge cases (i.e. don't check the bottom left pixel if we are on the left edge of the image)
		if curPixel[1] == originalImage.height-1 and curPixel[0] == originalImage.width-1:
			
			# Bottom right corner
			# Do nothing
			return newImage, recorded

		elif curPixel[1] == originalImage.height-1:
			
			# Bottom edge
			# Only check the pixel to the right
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[0] == 0:
			
			# Left edge
			# Check right, bottom, and bottom right
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[0] == originalImage.width-1:
			
			# Right edge
			# Check bottom, and bottom left
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		else:

			# Default case
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 2
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

	return newImage, recorded

# Returns an array of all the characters to be read through the OCR algorithm
# Takes a grayscale image as the input
def charactersToRead(myImage):

	# Array of images of characters in myImage to run through OCR algorithm
	characters = []
	# Array of pixels already found
	recorded = []

	# Check all pixels to find any non-white ones
	for i in range(myImage.height):
		for j in range(myImage.width):

			# Pixel to test
			testPixel = myImage.getpixel((j,i))

			# If the pixel is non-white and has not already been found
			if testPixel != 255 and notRecorded(recorded, j, i):
				
				# A new character has been found in the image!
				# Create a blank new image to record the character (same height and width as the original)
				newImage = Image.new("L", (myImage.width, myImage.height), color=255)

				newImage, recorded = pixelSearch(myImage, newImage, recorded, [j, i])

				characters.append(copy.deepcopy(newImage))

	return characters

myImage = scaleImage(myImage, 120, 120)

print(myImage.width, myImage.height)

myChars = charactersToRead(myImage)

print(myChars)

for item in myChars:
	item.show()

myImage.show()
