"""
Programmer: Caleb Pudvar
    For information about program, 
    please refer to the readme
"""
from Board import *
from King  import *
import string

#=====================================================  

def main():
    
    print "\nWelcome to King Saul Checkers! [6x6, two Kings each]\n"
    
    
    B = Board()            # get new board  
    B.initializeBoard()    # set up starting board
    
    playGame(B)   
    
#===================================================== 

def getUserMove(possibleMoves):
    """
       Description: User enters desired move as (int int)
                    - will not pass until valid move has been entered
		    - possible moves stored within dictionary
    """    
    move = raw_input("Enter move(as:  # #): ")    
    
    while(move not in possibleMoves.keys()):	# while move isnt possible
	print "Not a valid entry. Try again"
	move = raw_input("Enter move(as:  # #): ")	
    
    return move

#===================================================== 

def playGame(board):
    depth = getDifficulty()		#get difficulty (ply)
    print board          		#starting board

    #I always go first! 
    isMe = True
    while (board.notOver()):		#while both teams have kings
	   
	    if(isMe):	 #my turn?	
		nextMoves = getAllChildren(board, 'h')		# build dictionary of all moves for human
		move = getUserMove(nextMoves)		        
		board = nextMoves[move]                         # update board given user move
		
		isMe = False                                    # set to computer's turn
	    else:
		#receive tuple from alpha/beta game tree given tuples and ply
		result = maxValue((-1000000000, board), (-99999999, board), (99999999, board), depth)   
		board = result[1]		                # update board given computer move

		print board		                        
		isMe = True  
		
    print "Game Over!"    
    
#===================================================== 

def getAllChildren(B, player):
    #print B
    dictionary = {}
    """
    for nextKing in board.whichKing.keys():
	print board.whichKing[nextKing]
    """
    
    if (player == 'h'):
	print "-------------------------------------"
	print "Potential Moves:"
    else:
	print "\n\nComputer moves:\n"
    for moveThisKing in B.whichKing.keys():
	newBoards = B.getKingMoves( B.whichKing[moveThisKing], player )
		    
	for nextBoard in newBoards:
	    if player == 'h':
		if (B.whichKing[moveThisKing].alive):
		    print "\tFROM", B.whichKing[ moveThisKing ].chinookNum, "TO", nextBoard.whichKing[ moveThisKing ].chinookNum
		    #print nextBoard
		    dictionary[str(B.whichKing[ moveThisKing ].chinookNum) + " " + str(nextBoard.whichKing[ moveThisKing ].chinookNum)] = nextBoard    
	    
    if (player == 'h'):
	print "-------------------------------------\n"			    
			         
    return dictionary

#=====================================================
def getDifficulty():
    
    """
    Description: Determines difficulty (ply) of the current game based on user input                 
    """     
    
    difficulty = ['1','2','3','4','5']
    print "1 -- Novice"
    print "2 -- Easy"
    print "3 -- Medium"
    print "4 -- Hard"
    print "5 -- Impossible"

    choice = raw_input("\nWhich difficulty would you like to play? ")  
	
    while choice not in difficulty:
	choice = raw_input("\nWhich difficulty would you like to play? ")
	    
    print "\nPlaying game at difficulty level: ", choice, " Good luck!\n" 
    
    return int(choice)
        
#===================================================== 

def maxValue(state, alpha, beta, depth):
    
    """
    Description: Recursion pair with minValue (see below)
                 Receives board, relative boardscores, and the ply of game. With 
		 this info, helps to determine computer's next best move		 
    """    

    if(depth == 0):
	score = staticEval(state[1])
	newTuple = (score, state[1])
	return newTuple              # return values for 'youngest' descendant
    
    else:
	for moveThisKing in state[1].whichKing.keys():
	    newBoards = state[1].getKingMoves( state[1].whichKing[moveThisKing], 'm' ) 
	    for board in newBoards:

		newScore = staticEval(board)
		toMin = (newScore, board)
		newTuple = minValue(toMin, alpha, beta, (depth - 1))
		a = alpha[0]
		t = newTuple[0]
		
		maxResult = (max(a, t), board)

		if ((alpha[0]) >= maxResult[0]):
		    return maxResult

    return maxResult

#=====================================================     

def minValue(state, alpha, beta, depth):
    
    """
    Description: Recursion pair with maxValue (see above)
                 Receives board, relative boardscores, and the ply of game. With 
		 this info, helps to determine computer's next best move		 
    """    

    if(depth == 0):
	score = staticEval(state[1])
	newTuple = (score, state[1])
	return newTuple               # return values for 'youngest' descendant

    else:
	for moveThisKing in state[1].whichKing.keys():
	    newBoards = state[1].getKingMoves( state[1].whichKing[moveThisKing], 'h' )
	    for board in newBoards:
		
		newScore = staticEval(board)
		toMax = (newScore, board)
		newTuple = maxValue(toMax, alpha, beta, (depth - 1))
		b = beta[0]
		t = newTuple[0]

		minResult = (min(b, t), board)

		if (alpha[0]) >= (minResult[0]):
		    return minResult
    return minResult

#===================================================== 

def staticEval(state):
    """
       Description: simple static evaluator. determines board score by computer's kings - player kings
                    where computer kings are worth twice as much as player kings
    """

    compKings = 2
    playerKings = 2
    
    for king in state.whichKing.keys():
	if(state.whichKing[king].who == 'm'):
	    if(state.whichKing[king].alive == False):
		compKings -= 1
	if(state.whichKing[king].who == 'h'):
	    if(state.whichKing[king].alive == False):
		playerKings -= 1	    

    score  = ( 2 * compKings) - playerKings
    return score   
    
#===================================================== 

#-----------\
# START HERE \
#-----------------------------------------------------	
if __name__ == '__main__':
    main()

#-----------------------------------------------------