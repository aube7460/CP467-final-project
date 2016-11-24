from PIL import Image
from whiteBlack import *

def padZeros(img):
    padded = Image.new("L", (img.width + 2, img.height + 2), color = 0) #create new image
    i = 0       #counter
    j = 0       #counter
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

def zsAlgorithm(myImage):

	deleting = True

	# Keep performing
	while deleting:

		toDelete = []

		# First sub-iteration
		for j in range(1, myImage.height-1):
			for i in range(1, myImage.width-1):

				# Check only if the pixel is black
				if myImage.getpixel((i,j))==0:

					# Get all of the surrounding pixel values in an array to work with
					surroundArray = []
					surroundArray.append(myImage.getpixel((i,j-1)))
					surroundArray.append(myImage.getpixel((i+1,j-1)))
					surroundArray.append(myImage.getpixel((i+1,j)))
					surroundArray.append(myImage.getpixel((i+1,j+1)))
					surroundArray.append(myImage.getpixel((i,j+1)))
					surroundArray.append(myImage.getpixel((i-1,j+1)))
					surroundArray.append(myImage.getpixel((i-1,j)))
					surroundArray.append(myImage.getpixel((i-1,j-1)))
		
					# Get the number of 01 patterns in the surrounding set A(P1)
					zeroOnePatterns = 0
					k = 0
					while k < len(surroundArray):
						# Check only if not the last element in the list
						if k < len(surroundArray)-1:
							if surroundArray[k] == 255 and surroundArray[k+1] == 0:
								zeroOnePatterns += 1
						# If the last element check the front (circular) not the following value (would be out of index error)
						else:
							if surroundArray[k] == 255 and surroundArray[0] == 0:
								zeroOnePatterns += 1
						k += 1

					# Get the number of non-zero neighbours of this pixel
					totalNonZero = 0
					for item in surroundArray:
						if item == 0:
							totalNonZero += 1

					# Check if the conditions are met to delete a pixel
					if totalNonZero >= 2 and totalNonZero <= 6 and zeroOnePatterns == 1 and (myImage.getpixel((i,j-1))==255 or myImage.getpixel((i+1,j))==255 or myImage.getpixel((i,j+1))==255) and (myImage.getpixel((i+1,j))==255 or myImage.getpixel((i,j+1))==255 or myImage.getpixel((i-1,j))==255):
						toDelete.append((i,j))

		# Make all the pixels specified to be deleted white (aka "delete" them)
		for item in toDelete:
			myImage.putpixel(item, 255)

		toDelete = []

		# Second sub-iteration
		for j in range(1, myImage.height-1):
			for i in range(1, myImage.width-1):

				# Check only if the pixel is black
				if myImage.getpixel((i,j))==0:

					# Get all of the surrounding pixel values in an array to work with
					surroundArray = []
					surroundArray.append(myImage.getpixel((i,j-1)))
					surroundArray.append(myImage.getpixel((i+1,j-1)))
					surroundArray.append(myImage.getpixel((i+1,j)))
					surroundArray.append(myImage.getpixel((i+1,j+1)))
					surroundArray.append(myImage.getpixel((i,j+1)))
					surroundArray.append(myImage.getpixel((i-1,j+1)))
					surroundArray.append(myImage.getpixel((i-1,j)))
					surroundArray.append(myImage.getpixel((i-1,j-1)))

					# Get the number of 01 patterns in the surrounding set A(P1)
					zeroOnePatterns = 0
					k = 0
					while k < len(surroundArray):
						# Check only if not the last element in the list
						if k < len(surroundArray)-1:
							if surroundArray[k] == 255 and surroundArray[k+1] == 0:
								zeroOnePatterns += 1
						# If the last element check the front (circular) not the following value (would be out of index error)
						else:
							if surroundArray[k] == 255 and surroundArray[0] == 0:
								zeroOnePatterns += 1
						k += 1

					# Get the number of non-zero neighbours of this pixel
					totalNonZero = 0
					for item in surroundArray:
						if item == 0:
							totalNonZero += 1

					# Check if the conditions are met to delete a pixel
					if totalNonZero >= 2 and totalNonZero <= 6 and zeroOnePatterns == 1 and (myImage.getpixel((i,j-1))==255 or myImage.getpixel((i+1,j))==255 or myImage.getpixel((i-1,j))==255) and (myImage.getpixel((i,j-1))==255 or myImage.getpixel((i,j+1))==255 or myImage.getpixel((i-1,j))==255):
						toDelete.append((i,j))

		# Make all the pixels specified to be deleted white (aka "delete" them)
		for item in toDelete:
			myImage.putpixel(item, 255)

		if len(toDelete) == 0:
			deleting = False

	return myImage