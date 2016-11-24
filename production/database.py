from PIL import Image
import mysql.connector
from euclideanDistance import *
from statMethod import divideImage
from scaling import *
from zsAlgorithm import *
from whiteBlack import *

# Adds all of the images in the numbers folder to the database
def addValuesToDB(db):

	cursor = db.cursor()

	for i in range(0,10):
		for j in range(1, 6):
			
			tempimage = Image.open("numbers/{0}_{1}.png".format(i, j)).convert("L")
			
			tempimage = convertBW(tempimage)	
			image = scaleImage(tempimage, 80, 80)
			image = padZeros(image)
			image = zsAlgorithm(image)
			temparray = divideImage(image)
			print(temparray)
			
			statement = "INSERT INTO features VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16})"\
			.format(temparray[0], temparray[1], temparray[2], temparray[3], temparray[4], temparray[5], temparray[6], temparray[7], temparray[8],\
					 temparray[9], temparray[10], temparray[11], temparray[12], temparray[13], temparray[14], temparray[15], i)
			cursor.execute(statement)
			db.commit()

	for i in range(26):
		for j in range(1, 6):
			LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

			tempimage = Image.open("numbers/{0}_{1}.png".format(LETTERS[i], j)).convert("L")
			
			tempimage = convertBW(tempimage)	
			image = scaleImage(tempimage, 80, 80)
			image = padZeros(image)
			image = zsAlgorithm(image)
			temparray = divideImage(image)
			print(temparray)
			
			statement = "INSERT INTO features VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, '{16}')"\
			.format(temparray[0], temparray[1], temparray[2], temparray[3], temparray[4], temparray[5], temparray[6], temparray[7], temparray[8],\
					 temparray[9], temparray[10], temparray[11], temparray[12], temparray[13], temparray[14], temparray[15], LETTERS[i])
			cursor.execute(statement)
			db.commit()

	cursor.close()

	return

# Adds all of the images in the numbers folder to the database
def addNumbersToDB(db):

	cursor = db.cursor()

	for i in range(0,10):
		for j in range(1, 6):
			
			tempimage = Image.open("numbers/{0}_{1}.png".format(i, j)).convert("L")
			
			tempimage = convertBW(tempimage)	
			image = scaleImage(tempimage, 80, 80)
			image = padZeros(image)
			image = zsAlgorithm(image)
			temparray = divideImage(image)
			print(temparray)
			
			statement = "INSERT INTO features VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16})"\
			.format(temparray[0], temparray[1], temparray[2], temparray[3], temparray[4], temparray[5], temparray[6], temparray[7], temparray[8],\
					 temparray[9], temparray[10], temparray[11], temparray[12], temparray[13], temparray[14], temparray[15], i)
			cursor.execute(statement)
			db.commit()

	cursor.close()

	return

# Returns a 3D array with each array containing two elements: 1) Array of the percentages for each zone 2) The character the array corresponds to
def selectFromDB(db):

	# Create the cursor
	cursor = db.cursor()
	
	# Query the database for all data
	query = "SELECT * FROM features"
	
	# Execute the query
	cursor.execute(query)
	
	# Get all the values in an array
	vals = cursor.fetchall()
	
	# Close the cursor. We don't need it anymore
	cursor.close()
	
	# Create result array
	result = []
	
	# Go through all of the values and create the array containing the values, breaking it down into the specified output format
	for val in vals:
		temp = []
		temp.append(val[0:16])
		temp.append(val[16])
		result.append(temp)
		
	return result

# Given the array returned from selectFromDb() and the test vector, this finds the character closest to the given vector
# Returns that vector
def findCharacter(test, values):

	minVal = [euclideanDistance(values[0][0], test), values[0][1]]

	for value in values:
		temp = euclideanDistance(value[0], test)
		if temp < minVal[0]:
			minVal[0] = temp
			minVal[1] = value[1]

	return minVal[1]

def DBChar(pixelArr):
	db = mysql.connector.connect(user='leun4090', host='hopper.wlu.ca', password='bigtop6', database='leun4090')

	# Get the values from the DB
	result = selectFromDB(db)

	db.close()

	# Determine what character the image best corresponds to
	myChar = findCharacter(pixelArr, result)

	return myChar

def DBInsert():

	db = mysql.connector.connect(user='leun4090', host='hopper.wlu.ca', password='bigtop6', database='leun4090')

	addValuesToDB(db)

	db.close()

	return

def DBInsertNumbers():

	db = mysql.connector.connect(user='leun4090', host='hopper.wlu.ca', password='bigtop6', database='leun4090')

	addNumbersToDB(db)

	db.close()

	return

def DBInsertChar(temparray, myChar):
	
	db = mysql.connector.connect(user='leun4090', host='hopper.wlu.ca', password='bigtop6', database='leun4090')

	cursor = db.cursor()

	statement = "INSERT INTO features VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, '{16}')"\
	.format(temparray[0], temparray[1], temparray[2], temparray[3], temparray[4], temparray[5], temparray[6], temparray[7], temparray[8],\
					 temparray[9], temparray[10], temparray[11], temparray[12], temparray[13], temparray[14], temparray[15], myChar)
	cursor.execute(statement)
	db.commit()

	cursor.close()

	db.close()

	return