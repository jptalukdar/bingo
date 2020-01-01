
import sys
import math
import logging
import zUtility

logger=logging.getLogger(__name__)

class MovesStats:
	def __init__(self,size):
		self.crossed="##"
		self.moveTypes={}
	def invalidMove(self,message="You have made an Illegal Move"):
		zUtility.message(message)
		self.countInvalid()
		return None
	def count(self, key="normal"):
		key=str(key).lower()
		if key in self.moveTypes:
			self.moveTypes[key]+=1
		else:
			self.moveTypes[key]=1
	def countInvalid(self):
		self.count("Invalid")

	def countValid(self):
		self.count("valid")

	def getCount(self,key=None):
		if key == None:
			for k in self.moveTypes:
				zUtility.message("\t{} : {}\n".format(k,moveTypes[k]))
		else:
			zUtility.message("\t{} : {}\n".format(k,moveTypes.get(k,"No Counter Exists")))

	
		
class Board:
	def __init__(self,size,height=None,width=None):
		self.boardConf=zUtility.createRandomList(size)
		self.setDimensions(height,width)
		self.size=size
	def setCrossed(self,marker):
		self.crossedCharacter = marker
	def isCrossed(self,index):
		if self.boardConf[index]==self.crossedCharacter:
			return True
		else:
			return False
	def setDimensions(self,height=None,width=None):
		size=len(self.boardConf)
		if (height == None and width == None) or (height == 0 or width ==0):
			height = math.floor(math.sqrt(size))
			width = math.ceil(math.sqrt(size))
		elif height != None:
			width = math.floor( size / height )
		elif width != None:
			height = math.floor( size / width )
		self.height= height
		self.width = width
	def getDimensions(self):
		return (self.height,self.width)
	def __getitem__(self, key):
		return self.boardConf[key]

	def __setitem__(self,key,value):
		self.boardConf[key]=value

	def __len__(self):
		return self.size

	def index(self,key):
		return self.boardConf.index(key)
	def checkRow(self,index):
		if self.checkRowCut(index) == self.width:
			return 1
		else:
			return 0
	def checkColumn(self,index):
		if self.checkColumnCut(index) == self.height:
			return 1
		else:
			return 0
	def checkLeftDiagonal(self,index):		#\
		if self.checkLeftDiagonalCut(index) == self.height:
			return 1
		else:
			return 0

	def checkLeftDiagonalCut(self,index):
		row = self.getRow(index)
		column = self.getColumn(index)
		crossedOut=0
		if row == column:		#Check Top to Bottom Diag \
			for i in range(0,self.size,self.width+1):
				if self.isCrossed(i) == True:
					crossedOut+=1
		return crossedOut


	def checkRightDiagonal(self,index):		#/
		if self.checkRightDiagonalCut(index) == self.height:
			return 1
		else:
			return 0

	def checkRightDiagonalCut(self,index):
		row = self.getRow(index)
		column = self.getColumn(index)
		
		crossedOut=0
		if (row + column +1) % self.width == 0:
			for i in ((i*self.width + self.width - i -1) for i in range(self.width)):
				if self.isCrossed(i) == True:
					crossedOut+=1

		return crossedOut
	#@deprecated
	def checkDiagonal(self,index):
		#TODO: For non-uniform board
		row = self.getRow(index)
		column = self.getColumn(index)
		
		
		if (row + column +1) % self.width == 0:
			logger.debug([((i*self.width + self.width - i -1) for i in range(self.width))])
			for i in ((i*self.width + self.width - i -1) for i in range(self.width)):
				if self.isCrossed(i) == False:
					return 0
		elif row == column:		#Check Top to Bottom Diag \
			for i in range(0,self.size,self.width+1):
				if self.isCrossed(i) == False:
					return 0
		else:
			return 0
		return 1

	def checkRowCut(self,index):
		row = self.getRow(index)
		
		crossedOut=0
		for i in range(self.width*row,self.width*(row+1)):
			if self.isCrossed(i) == True:
				crossedOut+=1
		return crossedOut
	def checkColumnCut(self,index):
		
		column = self.getColumn(index)
		
		logger.debug([*range(column,self.size,self.width)])
		crossedOut=0
		for i in range(column,self.size,self.width):
			if self.isCrossed(i) == True:
				crossedOut+=1
		return crossedOut	
	def getRow(self,index):
		row = math.floor(index / self.width)
		return row

	def getColumn(self,index):
		return 	index % self.width
	def checkDiagonalCuts(self,index):
		#TODO: For non-uniform board
		row = self.getRow(index)
		column = self.getColumn(index)
		
		crossedOut=0
		if (row + column +1) % self.width == 0:
			logger.debug([((i*self.width + self.width - i -1) for i in range(self.width))])
			for i in ((i*self.width + self.width - i -1) for i in range(self.width)):
				if self.isCrossed(i) == True:
					crossedOut+=1
		elif row == column:		#Check Top to Bottom Diag \
			for i in range(0,self.size,self.width+1):
				if self.isCrossed(i) == True:
					crossedOut+=1
		return crossedOut
	


class Player:
	def __init__(self,playerName="Player",size=5):
		size=size*size
		self.moves = MovesStats(size)
		self.board=Board(size)
		self.board.setCrossed(self.moves.crossed)
		self.size=size
		self.height,self.width=self.board.getDimensions()
		self.playerName=playerName
		self.cuts=0
		self.ai=False
	
	def displayStats(self):
		self.moves.getCount()
	def isAI(self):
		return self.ai
	def checkWinning(self,index):
				
		self.cuts+=self.board.checkRow(index)
		self.cuts+=self.board.checkColumn(index)
		self.cuts+=self.board.checkLeftDiagonal(index)
		self.cuts+=self.board.checkRightDiagonal(index)
		if self.cuts==self.width:
			return True
		else:
			return False

	def turn(self,number):
		if number > self.size or number <= 0:
			return self.moves.invalidMove("You have entered Invalid Number, Try again\n")
		try:		
			index=self.board.index(number)
			self.board[index]=self.moves.crossed
			return self.checkWinning(index)

		except ValueError:
			return self.moves.invalidMove("Number is already crossed out, Choose Another\n")
		
	def display(self,override=False):
		if self.ai == True and override==False:
			return None
		zUtility.message(self.playerName+": {}\n".format(self.cuts)) 
		self.displayBoard(self.board)
		
	def displayBoard(self,boardList):
		height,width=boardList.getDimensions()
		logger.debug("Height: {} , width={} ".format(height,width))
		for row in range(0,height):
			displayRow="\t|"
			#zUtility.message("\t{}\n".format("_"*(width*3+1)))
			for column in range(0,width):	
				displayRow+="{:2}|".format(boardList[row*width+column])
			zUtility.message(displayRow+"\n") 
			logger.debug(displayRow)   
		
