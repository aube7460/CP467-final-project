import math

# Euclidean Distance function
#        -----------------------------------------------------------
# d = \ / (q[0] - s[0])^2 + (q[1] - s[1])^2 + ... + (q[i] - s[i])^2
#      v
# inputs:
#	q - feature vector # 1
#	s - feature vector # 2
# outputs:
#	d - euclidean distance of q and s feature vector rounded to 4 decimal places
def euclideanDistance (q, s):
	d = 0								#initialize return variable
	i = 0								#initialize counter
	temp = 0							#initialize temp value for storing difference between the numbers at each index
	total = 0							#initialize total which will be incremented by each iteration of the for loop and the (q - s)^2 operation
	for i in range(len(q)):				#for each element in q and s
		temp = q[i] - s[i]				#subtract one from the other
		temp = math.pow(temp, 2)		#square the result 
		total = total + temp			#increment total with the result
		
	d = round(math.sqrt(total), 4)		#square root and round total to 4 decimal places
	
	return d