import copy
from PIL import Image

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
			# Check the pixel to the left, top left, top
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[1] == 0 and curPixel[0] == 0:
			
			# Top left corner
			# Check the pixel to the right, bottom, bottom right
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[1] == 0 and curPixel[0] == originalImage.width-1:
			
			# Top right corner
			# Check the pixel to the left, bottom, bottom left
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[1] == originalImage.height-1 and curPixel[0] == 0:
			
			# Bottom left corner
			# Check the pixel to the right, top, top right
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[1] == originalImage.height-1:
			
			# Bottom edge
			# Check the pixel to the left, top left, top, top right, right
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[1] == 0:

			# Top edge
			# Check left, bottom left, bottom, bottom right, right
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))

		elif curPixel[0] == 0:
			
			# Left edge
			# Check top, top right, right, bottom right, bottom
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			

		elif curPixel[0] == originalImage.width-1:
			
			# Right edge
			# Check top, top left, left, bottom left, bottom
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			

		else:

			# Default case
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] += 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[0] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] -= 1
			newImage, recorded = pixelSearch(originalImage, newImage, recorded, copy.deepcopy(curPixel))
			curPixel[1] -= 1
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