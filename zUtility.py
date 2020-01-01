import random
import sys
def createRandomList(size):
	randomList = [*range(1,size+1)]
	random.shuffle(randomList)
	return randomList


def message(msg=None):
	print(msg,end="")

