import mysql.connector

try:
	db = mysql.connector.connect(user='cp467', host='cp467ocrproject.cw8vw62f6dri.us-west-2.rds.amazonaws.com', password='imageprocessing', database='cp467final')

	cursor = db.cursor()

except mysql.connector.Error as err:
  print(err)
  db.close()