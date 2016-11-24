from PIL import Image

im = Image.open("grayscale.jpg")    #open image
filtered = Image.new("L", (im.width + 2, im.height + 2), color = 0) #create new image that is 2 pixels wider and taller than the original

filtered.paste(im, (1, 1), None) #copy image into new image with padding of a 1 pixel border around

filtered.show()     #show image for debugging purposes
print(filtered.width)
print(filtered.height)

print(filtered.getpixel((0, 0)))
