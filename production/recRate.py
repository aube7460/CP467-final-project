from PIL import Image
import subprocess
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

def getRecognitionRate():

	myFile = open("recRate-output.txt", "w+")

	total = [0] * 10
	correct = [0] * 10

	for i in range(0,10):
		print("The current number to test for is:",i, file=myFile)
		for j in range(1, 16):

			try:
				myImage = Image.open("test-nums/{0}_{1}.png".format(i, j)).convert("L")
				print('Image imported successfully', file=myFile)
			except IOError:
				print("Image import failed - file not found", file=myFile)

			myImage = myImage.resize((70,70))
			# Change to BW image
			myImage = convertBW(myImage)
			# Get the unique images
			images = charactersToRead(myImage)

			for image in images:
				original = copy.deepcopy(image)
				image = scaleImage(image, 120, 120)
				image = padZeros(image)
				image = zsAlgorithm(image)
				imageArray = divideImage(image)
				finalCharacter = DBChar(imageArray)
				print("The character in the image is:",finalCharacter, file=myFile)

				if finalCharacter == str(i):
					correct[i] += 1
				total[i] += 1

	print(correct, file=myFile)
	print(total, file=myFile)

	myTotal = 0
	myNum = 0
	for item in correct:
		myTotal += item/total[myNum]
		print(myNum, "-", item/total[myNum]*100, "percent", file=myFile)
		myNum += 1

	myTotal = myTotal / 10

	myTotal = myTotal * 100

	print("Total -", myTotal, "percent", file=myFile)

	myFile.close()

	return

def getCharRecognitionRate():

	myFile = open("recRate-output.txt", "w+")

	total = [0] * 26
	correct = [0] * 26
	LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

	for i in range(0,26):
		print("The current letter to test for is:", LETTERS[i], file=myFile)

		try:
			myImage = Image.open("test-nums/{0}.png".format(LETTERS[i])).convert("L")
			print('Image imported successfully', file=myFile)
		except IOError:
			print("Image import failed - file not found", file=myFile)

		myImage = myImage.resize((70,70))
		# Change to BW image
		myImage = convertBW(myImage)
		# Get the unique images
		images = charactersToRead(myImage)

		for image in images:
			original = copy.deepcopy(image)
			image = scaleImage(image, 120, 120)
			image = padZeros(image)
			image = zsAlgorithm(image)
			imageArray = divideImage(image)
			finalCharacter = DBChar(imageArray)
			print("The character in the image is:",finalCharacter, file=myFile)

			if finalCharacter == LETTERS[i]:
				correct[i] += 1
			total[i] += 1

	print(correct, file=myFile)
	print(total, file=myFile)

	myTotal = 0
	myNum = 0
	for item in correct:
		myTotal += item/total[myNum]
		print(myNum, "-", item/total[myNum]*100, "percent", file=myFile)
		myNum += 1

	myTotal = myTotal / 26

	myTotal = myTotal * 100

	print("Total -", myTotal, "percent", file=myFile)

	myFile.close()

	return

getRecognitionRate()

# p = subprocess.Popen(["/Applications/Preview.app", "test-nums/0_1.png"], shell=True)
# test = input("enter something will")
# p.kill()