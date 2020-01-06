import bingoGame
import logging
import bingoAI
import random
logging.basicConfig(format='%(levelname)s:%(funcName)s: %(message)s',filename='bingo.log',level=logging.DEBUG)

print("BINGO !!")
print("***********************")


def play(size=5, ai=False, player1Name=None, player2Name=None,simulate=False):
	winner=None
	if simulate:
		ai=True
		player1=bingoAI.AI(size=size)
	else:	
		player1= bingoGame.Player(player1Name,size)
	
	if ai:
		player2= bingoAI.AI(size=size)
	else:
		player2= bingoGame.Player(player2Name,size)

	print("{} vs {}".format(player1.playerName,player2.playerName))


	WINSTATUS=False
	while(WINSTATUS != True):
		while(True):
			player1.display(override=True)
			try:
				if player1.isAI():
					choice=player1.makeMove()
					print("Player {} Chooses {}: ".format(player1.playerName,choice))
				else:
					choice=int(input("Player {} Turn : ".format(player1.playerName)))
			except ValueError:
				continue
			WINSTATUS=player1.turn(choice)
			if WINSTATUS != None:
				if WINSTATUS == True:
					if player2.turn(choice):
						print("Match Drawn")
					else:
						print("Player {} Won ".format(player1.playerName))
						player1.display(override=True)
						winner=player1
					
				else:
					if player2.turn(choice):
						print("Player {} Won".format(player2.playerName))
						player2.display(override=True)
						WINSTATUS = True
						winner=player2
				break
		if WINSTATUS == True:
			break
		while(True):
			player2.display()
			try:			
				if player2.isAI():
					choice=player2.makeMove()
					print("Player {} Chooses {}: ".format(player2.playerName,choice))
				else:
					choice=int(input("Player {} Turn : ".format(player2.playerName)))
			except ValueError:
				continue
			
			WINSTATUS=player2.turn(choice)
			if WINSTATUS != None:
				if WINSTATUS == True:
					if player1.turn(choice):
						print("Match Drawn")
					else:
						print("Player {} Won".format(player2.playerName))
						player2.display(override=True)
						winner=player2
				else:
					if player1.turn(choice):
						print("Player {} Won".format(player1.playerName))
						WINSTATUS = True
						player1.display(override=True)
						winner=player1
				break
		
	
	print("BINGO!")
	if winner != None:
		print("Winner is {}".format(winner.playerName))
		winner.display(override=True)
	#if player2.isAI():
		#player2.displayInitialState()
		#player2.display(override=True)
	#	player2.displayStats()


if __name__=="__main__":
	while(True):
		try:		
			print("Press \nP to play with AI \nE to Exit\nS to Simulate\nany key to play as player ")
			choice = input().strip("\n").lower()
			logging.debug(choice)
			if choice == 'e':
				break
			elif choice == 'p':
				play(5,True,"You")
			elif choice == 's':
				play(5,simulate=True)			
			else:
				play(5,False,"Player One","Player Two") 
				
		except ValueError:
			print("You have entered an Invalid Choice, Please Try Again")		
		
