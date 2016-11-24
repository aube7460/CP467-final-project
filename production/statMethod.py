from PIL import Image
import math

def percentOfPixels(img):
    count = 0 
    imgSize = img.width*img.height
    
    for i in range(img.width-1):
        for j in range(img.height-1):
            pixelValue = img.getpixel((i,j))
            if pixelValue == 0:
                count += 1
    
    percent = count/imgSize
    
    return round(percent, 4)

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
    