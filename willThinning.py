from PIL import Image

# Pads the exterior of an image with white pixels
def padWhite(img):

	padded = Image.new("L", (img.width + 2, img.height + 2), color = 0) #create new image
	i = 0
	j = 0
	for i in range(0, padded.width):
		for j in range(0, padded.height):
			#top left
			if (i == 0 and j == 0):
				padded.putpixel((i, j), 255)   #pad top left pixel of padded image with top left pixel of original image
			#top right
			elif (i == padded.width-1 and j == 0):    
				padded.putpixel((i, j), 255)   #pad top right pixel of padded image with top right pixel of original image
			#bottom left
			elif (i == 0 and j == padded.height-1):
				padded.putpixel((i, j), 255)   #pad bottom left pixel of padded image with top right pixel of original image
			#bottom right
			elif (i == padded.width-1 and j == padded.height-1):
				padded.putpixel((i, j), 255)   #pad bottom right pixel of padded image with top right pixel of original image
			#left side
			elif (i == 0):
				padded.putpixel((i, j), 255) #pad left side of padded image with pixels along left side of original image
			#right side
			elif (i == padded.width-1):
				padded.putpixel((i, j), 255)   #pad right side of padded image with pixels along right side of original image
			#top side
			elif (j == 0):
				padded.putpixel((i, j), 255)     #pad top side of padded image with pixels along top side of original image
			#bottom side
			elif (j == padded.height-1):
				padded.putpixel((i, j), 255)      #pad bottom side of padded image with pixels along bottom side of original image
			#inside pixels
			else:
				padded.putpixel((i, j), img.getpixel((i-1, j-1)))       #pad the rest of the padded image with the pixels from the rest of the original image
	return padded

def removeExterior(myImage):


	return myImage

def willThinning(myImage):
	
	changes = True

	# Pad the image exterior with white pixels
	myImage = padWhite(myImage)

	myImage.show()

	while changes:

		# Initialize to false, if changes are made it will be changed and the 20 rules will be applied again
		changes = False

		for i in range(myImage.width):
			for j in range(myImage.height):
				print()
	# Removes the pixels on the outside of the image
	myImage = removeExterior(myImage)

	return myImage