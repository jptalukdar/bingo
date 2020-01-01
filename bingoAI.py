import bingoGame
import logging
import random
import sys
import copy
logger=logging.getLogger(__name__)

class AI(bingoGame.Player):
	def __init__(self,playerName=None,size=5):
		playerName=self.definePlayerName(playerName)
		self.heuristicMap=[0 for i in range(0,size*size)]
		super().__init__(playerName,size)
		self.initialState=copy.deepcopy(self.board)
		self.ai=True
		logger.info(self.playerName)
	def displayInitialState(self):
		super().displayBoard(self.initialState)

	def definePlayerName(self,playerName):
		if playerName != None:
			return playerName
		playerList=["Shaun","Jean","Jeet","Gaurav","Akash","Shalini","Priya","Meghna","Nandu"]
		return random.choice(playerList)
	def calculateHeuristic(self,index):
		if self.board.isCrossed(index):
			return -1
		value=0.0		
		value+=self.board.checkRowCut(index) / self.width
		value+=self.board.checkColumnCut(index) / self.height
		value+=self.board.checkLeftDiagonalCut(index) / self.height
		value+=self.board.checkRightDiagonalCut(index) / self.height
		return value
		
	def calculateHeuristicMap(self):
		for i in range(0,self.size):
			self.heuristicMap[i]=self.calculateHeuristic(i)
		logger.info(self.heuristicMap)
	
	def makeMove(self):
		self.calculateHeuristicMap()
		maxValue = max(self.heuristicMap)
		logger.debug(maxValue)
		possibleMoves=[]
		for index in range(0,self.size):
			if self.heuristicMap[index] == maxValue:
				possibleMoves.append(self.board[index])
		logger.debug(possibleMoves)
		return random.choice(possibleMoves)
		
