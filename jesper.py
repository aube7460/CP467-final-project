import sys
import time
import math
from PIL import Image

def percentOfPixels(img):
    count = 0 
    imgSize = img.width*img.height
    
    for i in range(img.width-1):
        for j in range(img.height-1):
            pixelValue = img.getpixel((i,j))
            if pixelValue == 0:
                count += 1
    
    percent = count/imgSize
    
    return percent 

##         w25 w50 w75
##       --- --- --- ---
##      | q1| q2| q3| q4|
##  h25  --- --- --- ---
##      | q5| q6| q7| q8|
##  h50  --- --- --- ---
##      | q9|q10|q11|q12|
##  h75  --- --- --- ---
##      |q13|q14|q15|q16|
##       --- --- --- ---

# Divides the image into 16 equal sections as individual Image objects
# Input: img - Image to be divided
# Output: q - array of Image's that make up the 16 cropped images

def divideImage(img):
    i = 0                               #counter
    q = []
    feature = []
    w25 = math.ceil(img.width / 4)      #1/4 of image's width
    w50 = math.ceil(img.width / 2)      #1/2 of image's width
    w75 = math.ceil(img.width * 0.75)   #3/4 of image's width

    h25 = math.ceil(img.height / 4)     #1/4 of image's height
    h50  = math.ceil(img.height / 2)    #1/2 of image's height
    h75 = math.ceil(img.height * 0.75)  #3/4 of image's height

    #First Row
    q.append(img.crop((0, 0, w25, h25)))
    q.append(img.crop((w25, 0, w50, h25)))
    q.append(img.crop((w50, 0, w75, h25)))
    q.append(img.crop((w75, 0, img.width, h25)))
    #Second Row
    q.append(img.crop((0, h25, w25, h50)))
    q.append(img.crop((w25, h25, w50, h50)))
    q.append(img.crop((w50, h25, w75, h50)))
    q.append(img.crop((w75, h25, img.width, h50)))
    #Third Row
    q.append(img.crop((0, h50, w25, h75)))
    q.append(img.crop((w25, h50, w50, h75)))
    q.append(img.crop((w50, h50, w75, h75)))
    q.append(img.crop((w75, h50, img.width, h75)))
    #Fourth Row
    q.append(img.crop((0, h75, w25, img.height)))
    q.append(img.crop((w25, h75, w50, img.height)))
    q.append(img.crop((w50, h75, w75, img.height)))
    q.append(img.crop((w75, h75, img.width, img.height)))

    for i in range(len(q)):
        feature.append(percentOfPixels(q[i]))

    return feature

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
        
    for n in range(len(imgArr)):
        print (imgArr[n])
        print ("\n")
        
    return imgArr

# Input:
#    myImage: the padded image to apply the filter to
#    matrix: the matrix to use to multiply the image by
# Output:
#    Filtered image
def applyFilter(img, kernel):
    i = 0
    j = 0
    filtered = Image.new("L", (img.width - 2, img.height - 2))  #create new image

    imageArray = []
    
    for i in range(1, img.width - 1):                        #for every pixel within padding
        for j in range(1, img.height - 1):
            del imageArray[:]                                #clear imageArray each loop
            imageArray.append(img.getpixel((i-1, j-1)))      #populate imageArray with top left pixel
            imageArray.append(img.getpixel((i, j-1)))        #populate imageArray with top middle pixel
            imageArray.append(img.getpixel((i+1, j-1)))      #populate imageArray with top right pixel
            imageArray.append(img.getpixel((i-1, j)))        #populate imageArray with middle left pixel
            imageArray.append(img.getpixel((i, j)))          #populate imageArray with middle pixel
            imageArray.append(img.getpixel((i+1, j)))        #populate imageArray with middle right pixel
            imageArray.append(img.getpixel((i-1, j+1)))      #populate imageArray with bottom left pixel
            imageArray.append(img.getpixel((i, j+1)))        #populate imageArray with bottom middle pixel
            imageArray.append(img.getpixel((i+1, j+1)))      #populate imageArray with bottom right pixel
            filtered.putpixel((i- 1, j- 1), convolute(imageArray, kernel))    #write result of convolution to new image
    return filtered

# Input:
#   imageArray - array containing the 9 pixel grayscale values
#   kernel - kernel matrix used for the convolution
def convolute(imageArray, kernel):
    temp = 0        #used to store current convolution sum
    
    for i in range(0, len(imageArray)):
        temp = temp + (imageArray[i]*kernel[i])    #increment temp by result of image pixel * kernel pixel

    return math.floor(temp)

#contains the 20 rules for thinning.
def thinning(img):
    
    temp = Image.new("1", (img.width-1, img.height-1))  #create new image
    pixelCounter = 0                                    #Keep track of how many pixels have been checked
    deleted = True                                      #boolean variable to determine if a pixel is deleted
    count = 0                                           #keeps track of how many pixels have been deleted in one iteration
    size = (img.width-1) * (img.height-1)               #The size of the image to compare to the pixel counter
    imgA = []                                           #used to get the pixels around the pixel in question
    
    while deleted:                                      #loop while there are still pixels being deleted
        
        deleted = False                                 #initially set it to false 
        
        for i in range(0, img.width-1):                         #for every pixel 
            for j in range(0, img.height-1):
                del imgA[:]                                     #delete the array contents 

                if i == 0 or j == 0:                            #if the index is out of bounds, set the pixel to white
                    imgA.append(255)
                else:               
                    imgA.append(img.getpixel((i-1, j-1)))       #populate imageArray with top left pixel
                    
                if j == 0:                                      #if the index is out of bounds, set the pixel to white
                    imgA.append(255)
                else:
                    imgA.append(img.getpixel((i, j-1)))         #populate imageArray with top middle pixel
                    
                if j == 0:                                      #if the index is out of bounds, set the pixel to white
                    imgA.append(255)    
                else:
                    imgA.append(img.getpixel((i+1, j-1)))       #populate imageArray with top right pixel
                
                if  i == 0:                                     #if the index is out of bounds, set the pixel to white
                    imgA.append(255)
                else:   
                    imgA.append(img.getpixel((i-1, j)))         #populate imageArray with middle left pixel
                    
                imgA.append(img.getpixel((i, j)))               #populate imageArray with middle pixel
                imgA.append(img.getpixel((i+1, j)))             #populate imageArray with middle right pixel
                
                if i == 0:                                      #if the index is out of bounds, set the pixel to white
                    imgA.append(255)
                else:
                    imgA.append(img.getpixel((i-1, j+1)))       #populate imageArray with bottom left pixel
                    
                imgA.append(img.getpixel((i, j+1)))             #populate imageArray with bottom middle pixel
                imgA.append(img.getpixel((i+1, j+1)))           #populate imageArray with bottom right pixel
                                        
                #rule 1
                if (imgA[0]==0 and imgA[3]==0 and imgA[4]==0 and imgA[6]==0 and imgA[7]==0 and imgA[2]==255 and imgA[5]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                
                #rule 2
                elif (imgA[0]==0 and imgA[1]==0 and imgA[3]==0 and imgA[4]==0 and imgA[6]==0 and imgA[5]==255 and imgA[8]==255):
                    temp.putpixel((i,j),255)  
                    deleted = True              #deleted the pixel
                #rule 3 
                elif (imgA[0]==0 and imgA[1]==0 and imgA[2]==0 and imgA[4]==0 and imgA[5]==0 and imgA[6]==255 and imgA[7]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 4
                elif (imgA[0]==0 and imgA[1]==0 and imgA[2]==0 and imgA[3]==0 and imgA[4]==0 and imgA[7]==255 and imgA[8]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                
                #rule 5
                elif (imgA[0]==0 and imgA[3]==0 and imgA[4]==0 and imgA[2]==255 and imgA[5]==255 and imgA[7]==255 and imgA[8]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 6 
                elif (imgA[0]==0 and imgA[1]==0 and imgA[4]==0 and imgA[5]==255 and imgA[6]==255 and imgA[7]==255 and imgA[8]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 7
                elif (imgA[0]==0 and imgA[1]==0 and imgA[2]==0 and imgA[3]==0 and imgA[4]==0 and imgA[6]==0 and imgA[7]==0 and imgA[8]==0 and imgA[5]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 8
                elif (imgA[0]==0 and imgA[1]==0 and imgA[2]==0 and imgA[3]==0 and imgA[4]==0 and imgA[5]==0 and imgA[6]==0 and imgA[8]==0 and imgA[7]==255):
                    temp.putpixel((i,j),255) 
                    deleted = True              #deleted the pixel
                    
                #rule 9
                elif (imgA[3]==0 and imgA[4]==0 and imgA[6]==0 and imgA[1]==255 and imgA[2]==255 and imgA[5]==255 and imgA[8]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 10
                elif (imgA[4]==0 and imgA[6]==0 and imgA[7]==0 and imgA[0]==255 and imgA[1]==255 and imgA[2]==255 and imgA[5]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                #rule 11
                elif (imgA[1]==0 and imgA[2]==0 and imgA[4]==0 and imgA[3]==255 and imgA[6]==255 and imgA[7]==255 and imgA[8]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                
                #rule 12
                elif (imgA[2]==0 and imgA[4]==0 and imgA[5]==0 and imgA[0]==255 and imgA[3]==255 and imgA[6]==255 and imgA[7]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                                
                #rule 13 
                elif (imgA[4]==0 and imgA[7]==0 and imgA[8]==0 and imgA[0]==255 and imgA[1]==255 and imgA[2]==255 and imgA[3]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 14
                elif (imgA[4]==0 and imgA[5]==0 and imgA[8]==0 and imgA[0]==255 and imgA[1]==255 and imgA[3]==255 and imgA[6]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                
                #rule 15
                elif (imgA[0]==0 and imgA[1]==0 and imgA[2]==0 and imgA[4]==0 and imgA[5]==0 and imgA[6]==0 and imgA[7]==0 and imgA[8]==0 and imgA[3]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 16 
                elif (imgA[0]==0 and imgA[2]==0 and imgA[3]==0 and imgA[4]==0 and imgA[5]==0and imgA[6]==0 and imgA[7]==0 and imgA[8]==0 and imgA[1]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 17
                elif (imgA[2]==0 and imgA[4]==0 and imgA[5]==0 and imgA[7]==0 and imgA[8]==0 and imgA[0]==255 and imgA[3]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 18
                elif (imgA[1]==0 and imgA[2]==0 and imgA[4]==0 and imgA[5]==0 and imgA[8]==0 and imgA[3]==255 and imgA[6]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 19
                elif (imgA[4]==0 and imgA[5]==0 and imgA[6]==0 and imgA[7]==0 and imgA[8]==0 and imgA[0]==255 and imgA[1]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                    
                #rule 20
                elif (imgA[3]==0 and imgA[4]==0 and imgA[6]==0 and imgA[7]==0 and imgA[8]==0 and imgA[1]==255 and imgA[2]==255):
                    temp.putpixel((i,j),255)
                    deleted = True              #deleted the pixel
                else:
                    temp.putpixel((i,j),img.getpixel((i,j)))            #if the pixel is not deleted, put it back into the image
                
                pixelCounter += 1               #add one to the pixel counter
                                
                if deleted:                     #if a pixel is deleted then add one to the deleted counter
                    count +=1
             
        if pixelCounter == size:                #if every pixel has been checked, check to see if any have been deleted
            if count > 0:                       #        if so, continue looping, if not then the image is thinned
                deleted = True
                i = 0                           # set i back to zero
                j = 0                           # set j back to zero
                pixelCounter = 0                # set the pixel counter back to zero 
                count = 0                       # reset count
                img = temp                      # move the image from the first iteration into the original image name, so the second iteration changes the first iteration
                                                #            not the original image
            else:
                deleted = False                 # no pixels were deleted so the image is thinned                  
    
    return temp
    
def padImage(img):
    padded = Image.new("L", (img.width + 2, img.height + 2), color = 0) #create new image
    i = 0       #counter
    j = 0       #counter
    for i in range(0, padded.width):
        for j in range(0, padded.height):
            #top left
            if (i == 0 and j == 0):
                padded.putpixel((i, j), img.getpixel((i, j)))   #pad top left pixel of padded image with top left pixel of original image
            #top right
            elif (i == padded.width-1 and j == 0):    
                padded.putpixel((i, j), img.getpixel((img.width-1, j)))   #pad top right pixel of padded image with top right pixel of original image
            #bottom left
            elif (i == 0 and j == padded.height-1):
                padded.putpixel((i, j), img.getpixel((i, img.height-1)))   #pad bottom left pixel of padded image with top right pixel of original image
            #bottom right
            elif (i == padded.width-1 and j == padded.height-1):
                padded.putpixel((i, j), img.getpixel((img.width-1, img.height-1)))   #pad bottom right pixel of padded image with top right pixel of original image
            #left side
            elif (i == 0):
                padded.putpixel((i, j), img.getpixel((i, j-1))) #pad left side of padded image with pixels along left side of original image
            #right side
            elif (i == padded.width-1):
                padded.putpixel((i, j), img.getpixel((img.width-1, j-1)))   #pad right side of padded image with pixels along right side of original image
            #top side
            elif (j == 0):
                padded.putpixel((i, j), img.getpixel((i-1, j)))     #pad top side of padded image with pixels along top side of original image
            #bottom side
            elif (j == padded.height-1):
                padded.putpixel((i, j), img.getpixel((i-1, img.height-1)))      #pad bottom side of padded image with pixels along bottom side of original image
            #inside pixels
            else:
                padded.putpixel((i, j), img.getpixel((i-1, j-1)))       #pad the rest of the padded image with the pixels from the rest of the original image
    return padded

def main ():
    #formatting for the main menu
    print("{0:-^50s}".format(''))
    print("{0:-^50s}".format('  Main Menu  '))
    print("{0:-^50s}".format(''))
    print("{0:^50s}".format('Welcome to the CP467 Final Project demo.'))
    print()
    
    # gives the user the choice of whether to run the program or end
    print("{0:^50s}".format('1. Filtering'))
    print("{0:^50s}".format('2. Thinning'))
    print("{0:^50s}".format('3. Scaling'))
    print("{0:^50s}".format('4. Getting features'))
    print("{0:^50s}".format('5. Quit'))
    
    #adds blanks lines and waits for the user input 
    print()
    menuoption = input('Enter your choice here: ')
    print()
    
    # menu option 1 is chosen
    if menuoption == "1":
        
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
    
        print("{0:-^50s}".format(''))
        print("{0:-^50s}".format('  Select your Filter  '))
        print("{0:-^50s}".format(''))
        print("{0:^50s}".format('1. High Pass Filter'))
        print("{0:^50s}".format('2. Low Pass Filter'))
        
        filteroption = input('Enter your choice here: ')

        if filteroption == "1":
            kernel = [-1, -1, -1, -1, 8, -1, -1, -1, -1]
        elif filteroption == "2":
            kernel = [1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9, 1/9]
        #end if
        imgBase.show()        
        imgPadded = padImage(imgBase) #pad input image
        imgFiltered = applyFilter(imgPadded, kernel)    #filters image
        imgFiltered.show()              #show filtered image
        imgFiltered.save("filteredimage.jpg")
        
    elif menuoption == "2":
        # Gets the file from the user
        filename = input('Please enter the filename for the image you\'d like to use: ')
        
        # Opens file and converts the image to black and white
        imgBase = Image.open(filename).convert("1")
        imgBase.show()
        
        # Thins the image
        imgThinned = thinning(imgBase)
        imgThinned.show()
        print ("done")
    elif menuoption == "3":
        print("opion 3")
    # menu option 3 is chosen
    elif menuoption == "4":
        print("Getting features")
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

        print(divideImage(imgBase))
    elif menuoption == "5":
        # exits the program
        print("Quitting program..")
        time.sleep(1.5)
        sys.exit
        
main()
