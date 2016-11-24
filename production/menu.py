from PIL import Image
from padding import *
from filter import *
from thinning import *
from scaling import *
from whiteBlack import *
from multiCharacters import *
from statMethod import *
from database import *
from zsAlgorithm import *
import time
import sys
import copy

def menu ():
	
	while True:
		#formatting for the main menu
		print("{0:-^50s}".format(''))
		print("{0:-^50s}".format('  Main Menu  '))
		print("{0:-^50s}".format(''))
		print("{0:^50s}".format('Welcome to the CP467 Final Project.'))
		print()
		
		# gives the user the choice of whether to run the program or end
		print("{0:^50s}".format('1. OCR System'))
		print("{0:^50s}".format('2. Filtering'))
		print("{0:^50s}".format('3. Thinning'))
		print("{0:^50s}".format('4. Scaling'))
		print("{0:^50s}".format('5. Multiple Characters'))
		print("{0:^50s}".format('6. Zoning'))
		print("{0:^50s}".format('7. Character Recognition'))
		print("{0:^50s}".format('8. Quit'))
		
		#adds blanks lines and waits for the user input 
		print()
		menuoption = input('Enter your choice here: ')
		print()
		
		if menuoption == "1":

			while True:
				# gets the filename from the user, opens the file, and tells user it imported successfully
				filename = input('Please enter the filename for the image you\'d like to use: ')

				try:
					myImage = Image.open(filename).convert("L")
					print('')
					print('Image imported successfully')
					print('')
					break
				except IOError:
					print("Image import failed - file not found")

			myImage = myImage.resize((70,70))

			# Change to BW image
			myImage = convertBW(myImage)
			
			myImage.show()

			# Get the unique images
			images = charactersToRead(myImage)

			for image in images:
				original = copy.deepcopy(image)
				image = scaleImage(image, 120, 120)
				image = padZeros(image)
				image = zsAlgorithm(image)
				imageArray = divideImage(image)
				finalCharacter = DBChar(imageArray)
				print("\nThe character in the image is:",finalCharacter,"\n")
				original.show()
				
				noErrors = True

				while noErrors:

					correct = input("Is this the correct character? (y/n) ")

					if correct == "y":
						print("Thank you for your feedback.")
						noErrors = False
					elif correct == "n":
						correctChar = input("What was the correct character? ")
						DBInsertChar(imageArray, correctChar)
						print("Database updated. Thank you for your feedback.")
						noErrors = False
					else:
						print("That is not a valid input please try again.\n")

			print("\nComplete\n")

		elif menuoption == "2":
			
			while True:
				# gets the filename from the user, opens the file, and tells user it imported successfully
				filename = input('Please enter the filename for the image you\'d like to use: ')

				try:
					imgBase = Image.open(filename).convert("L")
					print('')
					print('Image imported successfully')
					print('')
					break
				except IOError:
					print("Image import failed - file not found")
			
			while True:

				print("{0:-^50s}".format(''))
				print("{0:-^50s}".format('	Select your Filter	'))
				print("{0:-^50s}".format(''))
				print("{0:^50s}".format('1. Edge Detection'))
				print("{0:^50s}".format('2. Blur image'))
				print("{0:^50s}".format('3. Sharpen image'))
				print("{0:^50s}".format('4. Left Sobel'))
				print("{0:^50s}".format('5. Right Sobel'))
				print("{0:^50s}".format('6. Custom'))
				

				print()
				filteroption = input('Enter your choice here: ')
				print()

				if filteroption == "1":
					kernel = [-1, -1, -1, -1, 8, -1, -1, -1, -1]
					break
				elif filteroption == "2":
					kernel = [1/18, 1/8, 1/18, 1/8, 1/4, 1/8, 1/18, 1/8, 1/16]
					break
				elif filteroption == "3":
					kernel = [0, -1, 0, -1, 5, -1, 0, -1, 0]
					break
				elif filteroption == "4":
					kernel = [1, 0, -1, 2, 0, -2, 1, 0, -1]
					break
				elif filteroption == "5":
					kernel = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
					break
				elif filteroption == "6":
					kernel = []
					print("Please enter the 9 kernel values from top left to bottom right as each prompt comes up")
					print("Please only enter in integers and decimals (no fractions)")
					kernelinput = float(input("Please enter the 1st value: "))
					kernel.append(kernelinput)
					kernelinput = float(input("Please enter the 2nd value: "))
					kernel.append(kernelinput)
					kernelinput = float(input("Please enter the 3rd value: "))
					kernel.append(kernelinput)
					for m in range(4, 10):
						kernelinput = float(input("Please enter the {0}th value: ".format(m)))
						kernel.append(kernelinput)
					break
				else:
					print("Invalid option. Please try again.\n")
			#end if
			imgBase.show()		  
			imgPadded = padImage(imgBase) #pad input image
			imgFiltered = applyFilter(imgPadded, kernel)	#filters image
			imgFiltered.show()				#show filtered image
			
		elif menuoption == "3":

			while True:
				# Gets the file from the user
				filename = input('Please enter the filename for the image you\'d like to use: ')
				
				try:
					# Opens file and converts the image to black and white
					imgBase = Image.open(filename).convert("L")
					
					imgBase = imgBase.resize((120,120))

					# Change to BW image
					myImage = convertBW(imgBase)

					while True:

						print("{0:-^50s}".format(''))
						print("{0:-^50s}".format('	Select your Thinning Algorithm	'))
						print("{0:-^50s}".format(''))
						print("{0:^50s}".format('1. ZS Algorithm'))
						print("{0:^50s}".format('2. 20 Rules Algorithm'))

						print()
						thinningOption = input('Enter your choice here: ')
						print()

						if thinningOption == "1":
							
							myImage.show()
							myImage = padZeros(myImage)
							myImage = zsAlgorithm(myImage)
							myImage.show()
							break

						elif thinningOption == "2":
							
							myImage.show()
							myImage = padZeros(myImage)
							myImage = thinning(myImage)
							myImage.show()
							break

						else:
							print("Invalid option. Please try again.\n")

					print("\nComplete.\n")
					break
				except IOError:
					print("Image import failed - file not found")

		elif menuoption == "4":

			while True:
				# Gets the file from the user
				filename = input('Please enter the filename for the image you\'d like to use: ')
				
				try:
					# Opens file and converts the image to grayscale
					imgBase = Image.open(filename).convert("L")
					imgBase.show()
					
					# Thins the image
					imgThinned = scaleImage(imgBase, 120, 120)
					imgThinned.save("tests/scaleoutput.bmp")
					imgThinned.show()

					print("\nComplete.\n")
					break
				except IOError:
					print("Image import failed - file not found")

		elif menuoption == "5":

			while True:
				# Gets the file from the user
				filename = input('Please enter the filename for the image you\'d like to use: ')
				
				try:
					# Opens file and converts the image to grayscale
					imgBase = Image.open(filename).convert("L")
					
					imgBase = imgBase.resize((70,70))
					
					# Get the unique images
					images = charactersToRead(imgBase)
					
					imgBase.show()
					
					for image in images:
						image.show()

					print("\nComplete.\n")
					break
				except IOError:
					print("Image import failed - file not found")

		elif menuoption == "6":

			while True:
				# Gets the file from the user
				filename = input('Please enter the filename for the image you\'d like to use: ')
				
				try:
					# Opens file and converts the image to grayscale
					imgBase = Image.open(filename).convert("L")
					
					image = scaleImage(imgBase, 120, 120)
					image = convertBW(image)
					image = padZeros(image)
					image = zsAlgorithm(image)
					image.show()
					imageArray = divideImage(image)
					print(imageArray)

					print("\nComplete.\n")
					break
				except IOError:
					print("Image import failed - file not found")

		elif menuoption == "7":

			while True:
				# Gets the file from the user
				filename = input('Please enter the filename for the image you\'d like to use: ')
				
				try:
					# Opens file and converts the image to grayscale
					imgBase = Image.open(filename).convert("L")

					image = scaleImage(imgBase, 120, 120)
					image = convertBW(image)
					image = padZeros(image)
					image = zsAlgorithm(image)
					imageArray = divideImage(image)
					
					result = DBChar(imageArray)

					print("\nThe character in the image is:",result,"\n")
					imgBase.show()
					break
				except IOError:
					print("Image import failed - file not found")

		elif menuoption == "8":
			# exits the program
			print("Quitting program.")
			break
		else:
			print()
			print("Not a valid menu option. Please try again.")
			print()
