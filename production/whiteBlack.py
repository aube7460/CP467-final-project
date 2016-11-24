from PIL import Image

# Converts an image from grayscale to black and white
def convertBW(myImage):

	for i in range(myImage.width):
		for j in range(myImage.height):
			if myImage.getpixel((i,j)) > 254:
				myImage.putpixel((i,j), 255)
			else:
				myImage.putpixel((i,j), 0)

	return myImage

# Converts pixels from white to black and vice versa
def invert(myImage):

	for i in range(myImage.width):
		for j in range(myImage.height):
			if myImage.getpixel((i,j)) == 255:
				myImage.putpixel((i,j), 0)
			else:
				myImage.putpixel((i,j), 255)

	return myImage
