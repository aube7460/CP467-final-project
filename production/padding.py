from PIL import Image

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