import random

def yarrow_stalk(verb = False):
	if verb: print("Fifty stalks, set one aside: --")
	sum = 0
	stalks = 49
	for i in range(3):
		left = random.randint(0, stalks)
		right = stalks - left
		if verb: print("-- {}  {}".format(left, right))
		remainder = 2
		left -= 1
		right -= 1
		if verb:
			print("Taking one from each side")
			print("-- ({}) {}  {}".format(remainder, left, right))
		left = left % 4
		right = right % 4
		if not left:
			left += 4
		if not right:
			right += 4
		if verb: print("-- ({}) {}  {}".format(remainder, left, right))
		remainder += left
		remainder += right
		
		if remainder > 6:
			score = 2
		else:
			score = 3
		sum += score
		if verb:
			print("-- ({}) leads to {}".format(remainder, score))
			print("Sum is {}".format(sum))
		last_stalks = stalks
		stalks = last_stalks - remainder
	return sum
	
	
if __name__=="__main__":
	dict = {6: 0, 7:0, 8: 0, 9:0}
	for i in range(10000):
		dict[yarrow_stalk()] += 1
	print (dict)
	
	yarrow_stalk(verb = True)