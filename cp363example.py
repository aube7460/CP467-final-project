'''
-------------------------------------------------------------------------------
CP363 - Inventory Management System
-------------------------------------------------------------------------------
Author: Jesper Leung
ID: 120754090
email: leun4090@mylaurier.ca
Date: 2015-03-24
-------------------------------------------------------------------------------
'''

import mysql.connector

db = mysql.connector.connect(user='root', host='localhost', password='1234', database='cp363inventorymanagement')

cursor = db.cursor()

menuoption = 0
#=====================================================================================================================
#                                                 MAIN MENU
#=====================================================================================================================
while(menuoption != 10): #while user hasn't decided to quit, loop back to main menu
    print ("Main Menu:")
    print ("1. Update product quantities")
    print ("2. Add or remove products")
    print ("3. Calculate monthly sales totals")
    print ("4. List all items below a specified stock level")
    print ("5. Product search")
    print ("6. List all items provided by a supplier")
    print ("7. List all items held at a certain warehouse")
    print ("8. List all items purchased by a certain customer")
    print ("9. List all sales made during a certain time period")
    print ("10. QUIT")
    menuoption = int(input()) #get menu option from user
    
#======================================================================================================================
#                                                OPTION ONE
#======================================================================================================================
    if menuoption == 1:
        print("Update product quantities")
        productid = input("Enter the product ID's quantity that you'd like to change\n") #get product's UPC from user
        quantity = int(input("Enter the new quantity: \n")) #get updated quantity from user
        
        statement='UPDATE Products SET quantity = {0} WHERE upc = {1}'.format(quantity, productid) #setup SQL statement
        cursor.execute(statement)
        
        print("---------------UPDATED ENTRY---------------")
        
        statement='SELECT * FROM Products WHERE upc = {0}'.format(productid) #get updated entry from database
        cursor.execute(statement)
        result = cursor.fetchall()
        
        print("{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])) #print out updated result
#======================================================================================================================
#                                                OPTION TWO
#======================================================================================================================
    elif menuoption == 2:
        print("Add or remove products")
        print("1. Add") 
        print("2. Remove")
        addremove = int(input()) #get menu option from user
        if addremove == 1: #if user entered 1, add product
            print("Add product")
            upc = input("Enter the UPC for the product\n") #get product's UPC from user
            productname = input("Enter the name of the product\n") #get product's name from user
            price = float(input("Enter the price of the product\n")) #get price of product from user
            quantity = int(input("Enter the quantity of the product\n")) #get stock level of new product
            supplier = input("Enter the name of the supplier\n") #get supplier name from user
            
            statement = "SELECT snum FROM Suppliers WHERE sname='{0}'".format(supplier) #setup SQL statement
            cursor.execute(statement)
            result = cursor.fetchall() #get supplier's ID number from table
            
            statement = "INSERT INTO Products values('{0}', '{1}', {2}, {3}, {4})".format(upc, productname, price, quantity, result[0][0]) #use supplier's number to generate SQL insertion statement
            cursor.execute(statement)
            
            print("---------------ADDED ENTRY---------------")
            statement = "SELECT * FROM Products".format(upc) #get updated entry from database 
            cursor.execute(statement)
            result = cursor.fetchall()
            
            for i in range(len(result)):
                print("{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4])) #print out updated result
            
        elif addremove == 2:
            print("Remove product")
            upc = input("Enter the UPC for the product to be deleted\n") #get product's UPC from user
            
            statement = "DELETE FROM Products WHERE upc = {0}".format(upc) #setup SQL statement
            cursor.execute(statement)
            print("---------------DELETED---------------") 
            
            statement = "SELECT * FROM Products".format(upc) #get updated entry from database 
            cursor.execute(statement)
            result = cursor.fetchall()
            
            for i in range(len(result)):
                print("{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4])) #print out updated result
#======================================================================================================================
#                                                OPTION THREE
#======================================================================================================================
    elif menuoption == 3:
        print("Monthly Sales Total")
        month = input("Enter the month that you'd like to calculate sales for\n") #get month from user
        year = input("Enter the year that you'd like to calculate sales for\n") #get year from user
        
        startdate = "{0}-{1}-1".format(year, month) #setup start date from user's information
        enddate = "{0}-{1}-31".format(year, month) #setup end date from user's information
        
        statement = "CREATE VIEW temp AS SELECT P.Price, C.Quantity FROM Products as P, Orders as O, Contain as C WHERE O.date > '{0}' AND O.date < '{1}' AND O.invoice = C.invoice AND C.upc = P.upc".format(startdate, enddate) #setup SQL statement
        cursor.execute(statement)
        
        statement = "SELECT sum(Price * Quantity) FROM temp" #use view from previous SQL statement to generate proper query
        cursor.execute(statement)
        
        result = cursor.fetchall()
        
        print("---------------TOTAL SALES---------------")
        print("${0}".format(result[0][0])) #printing results
#======================================================================================================================
#                                                OPTION FOUR
#======================================================================================================================        
    elif menuoption == 4:
        print("Low stock check")
        stocklevel = int(input("Please enter the stock level you'd like to search for\n")) #get stock level from user
        
        statement = "SELECT P.upc, P.pname, P.quantity, W.location, S.sname FROM Products as P, Warehouses as W, Suppliers as S WHERE P.quantity < {0} AND P.snum = S.snum AND S.wno = W.wno ORDER BY P.quantity ASC".format(stocklevel) #setup SQL statement
        cursor.execute(statement)
        
        result = cursor.fetchall()
        
        print("|{0:-^20}|{1:-^20}|{2:-^20}|{3:-^20}|{4:-^20}|".format("Product Name", "UPC", "Stock Level", "Supplier", "Warehouse Location")) #print header for table
        
        for i in range(len(result)):
            print ("|{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[i][1], result[i][0], result[i][2], result[i][4], result[i][3])) #print information as per user input
#======================================================================================================================
#                                                OPTION FIVE
#======================================================================================================================
    elif menuoption == 5:
        print("Product Search")
        print("1. Search by name")
        print("2. Search by UPC")
        searchop = int(input()) #get menu option from user
        if (searchop == 1): #if 1, user is searching by product name
            searchkey = input("Enter the name of the product you wish to search for\n") #get product name search key from user
            statement = "SELECT P.pname, P.upc, P.price, P.quantity, W.location FROM Products as P, Suppliers as S, Warehouses as W WHERE P.pname LIKE '%{0}%' AND P.snum = S.snum AND S.wno = W.wno".format(searchkey) #setup SQL statement
            cursor.execute(statement)
            
            result = cursor.fetchall()
            
            print("Products that match ""{0}".format(searchkey)) #print out information as per user input
            print("|{0:-^20}|{1:-^20}|{2:-^20}|{3:-^20}|{4:-^20}|".format("Product Name", "UPC", "Price", "Stock Level", "Warehouse Location"))
            for i in range(len(result)):
                print ("|{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
        elif (searchop == 2): #if 2, user is searching by UPC
            searchkey = input("Enter the UPC of the product you wish to search for\n") #get product UPC search key from user
            statement = "SELECT P.pname, P.upc, P.price, P.quantity, W.location FROM Products as P, Suppliers as S, Warehouses as W WHERE P.upc LIKE '%{0}%' AND P.snum = S.snum AND S.wno = W.wno".format(searchkey) #setup SQL statement
            cursor.execute(statement)
            
            result = cursor.fetchall()
            print("Products that match ""{0}".format(searchkey)) #print out information as per user input
            print("|{0:-^20}|{1:-^20}|{2:-^20}|{3:-^20}|{4:-^20}|".format("Product Name", "UPC", "Price", "Stock Level", "Warehouse Location"))
            for i in range(len(result)):
                print ("|{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
#======================================================================================================================
#                                                OPTION SIX
#======================================================================================================================
    elif menuoption == 6:
        print("List all items provided by supplier")
        suppliernum = input("Enter the supplier's ID number\n") #get supplier number from user
        
        statement = "SELECT P.pname, P.upc, P.price, W.location, S.sname FROM Products as P, Warehouses as W, Suppliers as S WHERE S.snum = {0} AND P.snum = S.snum AND S.wno = W.wno".format(suppliernum) #setup SQL statement
        cursor.execute(statement)
        
        result = cursor.fetchall()
        
        print("|{0:-^20}|{1:-^20}|{2:-^20}|{3:-^20}|".format("Product Name", "UPC", "Price", "Warehouse Location")) #print header for results table
        for i in range(len(result)): #print out information as per user input
            print ("|{0:^20}|{1:^20}|{2:^20}|{3:^20}|".format(result[i][0], result[i][1], result[i][2], result[i][3]))
#======================================================================================================================
#                                                OPTION SEVEN
#======================================================================================================================        
    elif menuoption == 7:
        print("List all items held at a warehouse")
        warehousenum = input("Enter the warehouse's ID number\n") #get warehouse number from user
        
        statement = "SELECT P.pname, P.upc, P.price, S.sname, W.location FROM Products as P, Warehouses as W, Suppliers as S WHERE W.wno = {0} AND P.snum = S.snum AND W.wno = S.wno".format(warehousenum) #setup SQL statement
        cursor.execute(statement)
        
        result = cursor.fetchall()
        
        print("|{0:-^20}|{1:-^20}|{2:-^20}|{3:-^20}|{4:-^20}".format("Product Name", "UPC", "Price", "Supplier", "Warehouse Location")) #print header for results table
        for i in range(len(result)): #print out information as per user input
            print ("|{0:^20}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|".format(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
#======================================================================================================================
#                                                OPTION EIGHT
#======================================================================================================================
    elif menuoption == 8:
        print("List all items purchased by a certain customer")
        customerid = int(input("Please enter the customer's ID\n")) #get customer number from user
        
        statement = "SELECT P.pname, N.quantity, P.price, O.date FROM Products as P, Contain as N, Orders as O, Customers as C WHERE C.cno = {0} AND C.cno = O.cno AND N.upc = P.upc AND O.invoice = N.invoice".format(customerid)
        cursor.execute(statement)
        
        result = cursor.fetchall()
        
        print("|{0:-^20}|{1:-^20}|{2:-^20}|".format("Product Name", "# Ordered", "Price")) #print header for results table
        for i in range(len(result)): #print out information as per user input
            print ("|{0:^20}|{1:^20}|{2:^20}|".format(result[i][0], result[i][1], result[i][2]))
#======================================================================================================================
#                                                OPTION NINE
#======================================================================================================================
    elif menuoption == 9:
        print("List all sales made during certain time period")
        sdate = input("Please enter the start date (YYYY-MM-DD)\n")
        edate = input("Please enter the end date (YYYY-MM-DD)\n")
        
        statement = "SELECT O.invoice, C.cname, P.pname, N.quantity, P.price, P.price * N.quantity FROM Orders as O, Customers as C, Products as P, Contain as N WHERE O.date > '{0}' AND O.date < '{1}' AND C.cno = O.cno AND O.invoice = N.invoice AND N.upc = P.upc".format(sdate, edate) #setup SQL statement
        cursor.execute(statement)
        
        result = cursor.fetchall()
        
        print("|{0:-^20}|{1:-^20}|{2:-^20}|{3:-^20}|{4:-^20}|{5:-^20}|".format("Invoice #", "Customer Name", "Product Name", "# Ordered", "Price", "Total",)) #print header for results table
        for i in range(len(result)): #print out information as per user input
            print ("|{0:^20}|{1:^20}|{2:^20}|{3:^20}|${4:^19}|${5:^19}|".format(result[i][0], result[i][1], result[i][2], result[i][3], result[i][4], result[i][5]))