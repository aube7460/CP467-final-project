UPDATE NOVEMBER 12th:
-Basic scaling algorithm implemented
-Thinning algorithm implemented but not tested
-Filtering function implemented (float + proper padding implemented, still need to figure out kernels for high pass, low pass, and mean filters)

Questions to ask Professor on November 13th:
-How do we approach the rotation problem?
-Show him our algorithm from front to back, to ensure that we have all components that we are required to have
-Show him our code (make sure using the Image library is OK and everything is being done as intended)
-Which filters do you want? Determine the kernel to use for high/low pass + mean
-

To Do:

- DONE !


OCR Program

Input:
-Image of a written character between 0 and 9 (inclusive)

Output:
-What digit that written character corresponds to (ascii)



Our Algorithm:

Input: Character digit image
1. Eliminate noise by applying several filters (high pass, low pass, mean filter) (also edge detection)
	-Ask him what filters we should use (i.e. all three, should mean be in there?)
	-Jesper (things in to do, add all three filters in)
2. Apply rotation algorithm (ask him what the fuck to do)
3. Apply Scaling algorithm (see below) (depends how well the noise elimination is)
	-Will (make sure the algorithm listed below is implemented and working probably)
4. Apply thinning algorithm (his algorithm)
	-Jason (make sure his algorithm is implemented and working)
5. Statistical pattern method to determine the percentage of pixels in each area. Final vector is all 9 values calculated.
6. See which character in our table the vector corresponds most accurately with. Output result to user
7. Find the number of connected regions in the input image (i.e. number of numbers written)

Functions:

-Eliminate noise
	-apply low pass filter
	-apply high pass filter
	-apply mean filter

		-Apply filter function --> takes in a kernel and outputs the image with the filtered applied to it

-Rotate the image
	
	?

-Scale the image to a uniform size

	-find the smallest x pixel not white then cut all pixels (x,y) such that x < pixel found
	-find the largest x pixel not white then cut all pixels (x,y) such that x > pixel found
	-find the smallest y pixel not white then cut all pixels (x,y) such that y < pixel found
	-find the largest y pixel not white then cut all pixels (x,y) such that y > pixel found

	-Scale the image to the set size (i.e. whatever remains from the cuts to 90x90)

-Thin the image

	-Apply his algorithm (20 if statements)

TOGETHER
-Transform the symbol to strokes
-Represent the strokes as a chain of codes

	-Statistical pattern method to determine the number of pixels in each section

-Apply mapping rules to make segments



-Final representation as a vector



-Change from vector to what the character is