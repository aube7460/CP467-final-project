from PIL import Image
import math

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
