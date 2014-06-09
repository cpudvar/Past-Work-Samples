# Board.py
""" Class for instances of Checker Board 
"""

import string
from King import *

class Board(object):
    """NxN board to play checkers"""
    
    # class members (all instances use these same values)    
    N = 6

    OPEN   = "     "
    CLOSED = "/////"
    
    POSITIONS = {}
    # from human players perspective (right-left, bottom to top)
    # converts Chinook number to [x][y] location
    POSITIONS[1] = [5,5]
    POSITIONS[2] = [5,3]
    POSITIONS[3] = [5,1]
    
    POSITIONS[4] = [4,4]
    POSITIONS[5] = [4,2]
    POSITIONS[6] = [4,0]
    
    POSITIONS[7] = [3,5]
    POSITIONS[8] = [3,3]
    POSITIONS[9] = [3,1]
    
    POSITIONS[10] = [2,4]
    POSITIONS[11] = [2,2]
    POSITIONS[12] = [2,0]
    
    POSITIONS[13] = [1,5]
    POSITIONS[14] = [1,3]
    POSITIONS[15] = [1,1]
    
    POSITIONS[16] = [0,4]
    POSITIONS[17] = [0,2]
    POSITIONS[18] = [0,0]

    #=====================================================  
    
        
    def __init__(self):
        """CTOR
        """
	
	# setup board (set bogus values)
	self.Board = [ 
	               [Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED], 
	               [Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN], 
	               [Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED],
	               [Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN],
	               [Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED],
	               [Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN,   Board.CLOSED, Board.OPEN]
	             ]
	
	# current location of empty space (0)
	self.mK1 = None
	self.mK2 = None
	self.hK1 = None
	self.hK2 = None
	
	self.whichKing = {}
	
    #=====================================================   
    
    def copyCTOR(self):
        """Copy CTOR
        """
	newBoard = Board()
	newBoard.Board = []
	for nextRow in self.Board:
	    newRow = []
	    for nextSpace in nextRow:
		newRow.append(nextSpace)
	    newBoard.Board.append(newRow)
	
	# current location of empty space (0)
	newBoard.mK1 = self.mK1.copyCTOR()
	newBoard.mK2 = self.mK2.copyCTOR()
	newBoard.hK1 = self.hK1.copyCTOR()
	newBoard.hK2 = self.hK2.copyCTOR()
	
	newBoard.whichKing = {}
	for moveThisKing in self.whichKing.keys():
	    newBoard.whichKing[ moveThisKing ] = self.whichKing[moveThisKing]
	      
	return newBoard  
    
    #=====================================================         
    def initializeBoard(self):
	""" set up a starting board
	"""
	self.mK1 = King("mK1", 0, 0)
	self.mK2 = King("mK2", 0, 2)
	
	self.hK1 = King("hK1", 5, 3)
	self.hK2 = King("hK2", 5, 5)
	
	# fill hash of kings; key==name, value==King object
	self.whichKing[ self.mK1.name ] = self.mK1
	self.whichKing[ self.mK2.name ] = self.mK2
	self.whichKing[ self.hK1.name ] = self.hK1
	self.whichKing[ self.hK2.name ] = self.hK2
	
	# place Chinook numbering scheme
	for chinookN in range(1,19):
	    xy = Board.POSITIONS[chinookN]
	    x = xy[0]
	    y = xy[1]
	    self.Board[x][y] = " " + str(chinookN) + " "
	    
	# place king names on board
	self.Board[ self.mK1.X ][ self.mK1.Y ] = self.mK1.name
	self.Board[ self.mK2.X ][ self.mK2.Y ] = self.mK2.name
	
	self.Board[ self.hK1.X ][ self.hK1.Y ] = self.hK1.name
	self.Board[ self.hK2.X ][ self.hK2.Y ] = self.hK2.name
	
	
    
    #=====================================================
    def __str__(self):
        """ sets up the current Board positions """
        
        b = "-------------------------------------\n"
        b = b + "|{0:5s}|{1:5s}|{2:5s}|{3:5s}|{4:5s}|{5:5s}|\n".format(self.Board[0][0], self.Board[0][1], self.Board[0][2], self.Board[0][3], self.Board[0][4], self.Board[0][5])
        b = b + "-------------------------------------\n"
        b = b + "|{0:5s}|{1:5s}|{2:5s}|{3:5s}|{4:5s}|{5:5s}|\n".format(self.Board[1][0], self.Board[1][1], self.Board[1][2], self.Board[1][3], self.Board[1][4], self.Board[1][5])
        b = b + "-------------------------------------\n"
        b = b + "|{0:5s}|{1:5s}|{2:5s}|{3:5s}|{4:5s}|{5:5s}|\n".format(self.Board[2][0], self.Board[2][1], self.Board[2][2], self.Board[2][3], self.Board[2][4], self.Board[2][5])
        b = b + "-------------------------------------\n"
        b = b + "|{0:5s}|{1:5s}|{2:5s}|{3:5s}|{4:5s}|{5:5s}|\n".format(self.Board[3][0], self.Board[3][1], self.Board[3][2], self.Board[3][3], self.Board[3][4], self.Board[3][5])
        b = b + "-------------------------------------\n"
        b = b + "|{0:5s}|{1:5s}|{2:5s}|{3:5s}|{4:5s}|{5:5s}|\n".format(self.Board[4][0], self.Board[4][1], self.Board[4][2], self.Board[4][3], self.Board[4][4], self.Board[4][5])
        b = b + "-------------------------------------\n"
        b = b + "|{0:5s}|{1:5s}|{2:5s}|{3:5s}|{4:5s}|{5:5s}|\n".format(self.Board[5][0], self.Board[5][1], self.Board[5][2], self.Board[5][3], self.Board[5][4], self.Board[5][5])
        b = b + "-------------------------------------\n"        
        
        return b 
    #=====================================================
    
    def notOver(self):
	""" determines if game is over by checking to see
	    if all kings on a team are killed
	"""
	compKings = 0
	playKings = 0

	for row in self.Board:
	    for cell in row:
		if(cell == ' mK1 ') or (cell == ' mK2 '):
		    compKings += 1
		if(cell == ' hK1 ') or (cell == ' hK2 '):
		    playKings += 1
    
	if (compKings == 0) or (playKings == 0):
	    return False
	else:
	    return True	
	
    #=====================================================
	
    def canJump(self, newB, moveThisKing, X, Y, player, direction, opponents, allKings, allMoves, oldChinook):
	"""
	Description: This function determines the possible moves a player can make
	             based on board configuration. 
		     
		     Returns: list of child boards
	"""	
	
	if(direction == 'nw'):
	    offsetX = -1          #travel direction (x)
	    offsetY = -1          #travel direction (y)
	    xOff = 1              #limit to jumping position (x)
	    yOff = 1              #limit to jumping position (y)
	elif(direction == 'sw'):
	    offsetX = -1
	    offsetY = 1
	    xOff = 1
	    yOff = 4	    
	elif(direction == 'ne'):
	    offsetX = 1
	    offsetY = -1
	    xOff = 4
	    yOff = 1	    
	elif(direction == 'se'):
	    offsetX = 1
	    offsetY = 1	
	    xOff = 4
	    yOff = 4	
	    
	if ((newB.Board[X+offsetX][Y+offsetY]) in opponents):        #if adjacent location is an opponent's king
	    if( (X != xOff)):                                        #if king would stay on board after jumping
		if(Y != yOff):                                     
		    if (newB.Board[X+ 2*offsetX][Y+ 2*offsetY]):     #if king would land in an open space
	
			jumpedChinook = King.CHINOOK_N[ ((moveThisKing.X+offsetX)*10) + (moveThisKing.Y+offsetY) ]	#record chinook value of jumped piece
			newB.Board[X][Y], newB.Board[X+ 2*offsetX][Y+ 2*offsetY] = newB.Board[X+ 2*offsetX][Y + 2*offsetY], newB.Board[X][Y] #move piece to destination
			newB.Board[X][Y] = ' ' + str(oldChinook)     #remove old king location
			newKing = moveThisKing.copyCTOR()
			newKing.X = X + 2*offsetX                    #update king position
			newKing.Y = Y + 2*offsetY
			    
			opponents[(newB.Board[X + offsetX][Y + offsetY])].alive = False      #kill jumped king
			newB.Board[X + offsetX][Y + offsetY] = " " + str(jumpedChinook)	     #remove jumped king from board		
			newKing.chinookNum = King.CHINOOK_N[ (newKing.X)*10 + newKing.Y ]    #update king's chinook value						  
			newB.whichKing[ moveThisKing.name ] = newKing                        
		
			allMoves.append(newB) #add child board to list of moves

	else:
	    newB.Board[X][Y], newB.Board[X + offsetX][Y + offsetY] = newB.Board[X + offsetX][Y + offsetY], newB.Board[X][Y] #swap board values
	    newB.Board[X][Y] = ' ' + str(oldChinook) #update board graphic
	    newKing = moveThisKing.copyCTOR()        #update king values
	    newKing.X = X + offsetX
	    newKing.Y = Y + offsetY
	    newKing.chinookNum = King.CHINOOK_N[ (newKing.X)*10 + newKing.Y ]
		  
	    newB.whichKing[ moveThisKing.name ] = newKing
	    allMoves.append(newB)
	
	return allMoves      #return child boards
	
    #===================================================== 
    
    def getKingMoves( self, moveThisKing, player ):
	# move this King on board in self
	opponents = {}                   #dictionary of opponent kings
	allKings = {}                    #dictionary of all kings on board
	newBoards = []
	X = moveThisKing.X               #X position of king
	Y = moveThisKing.Y               #Y position of king
	
	allKings[' mK1 '] = self.mK1
	allKings[' mK2 '] = self.mK2
	allKings[' hK1 '] = self.hK1
	allKings[' hK2 '] = self.hK2	
	
	if(player == 'h'):
	    opponents[' mK1 '] = self.mK1
	    opponents[' mK2 '] = self.mK2 
	if(player == 'm'):
	    opponents[' hK1 '] = self.hK1
	    opponents[' hK2 '] = self.hK2
	    
	oldChinook = King.CHINOOK_N[ (moveThisKing.X)*10 + moveThisKing.Y ] #record chinook location of king that will be moved
	
	if(player == moveThisKing.who): #move only one team's pieces
	# move NorthWest (NW) ?
	    if (X != 0 and Y != 0):
		if (not( (self.Board[X-1][Y-1])[1] == moveThisKing.who) ):
		    newB = self.copyCTOR()				    

		    newBoards = self.canJump(newB, moveThisKing, X, Y, player, 'nw', opponents, allKings, newBoards, oldChinook)
    
	    #Move NorthEast (NE)?
	    if (X != 5 and Y != 0):
		if not( (self.Board[X+1][Y-1])[1] == moveThisKing.who):
		    newB = self.copyCTOR()
		    		    			
		    newBoards = self.canJump(newB, moveThisKing, X, Y, player, 'ne', opponents, allKings, newBoards, oldChinook)
					
	    #Move SouthWest (SW)?
	    if (X != 0 and Y != 5):
		if not( (self.Board[X-1][Y+1])[1] == moveThisKing.who):
		    newB = self.copyCTOR()
		    
		    newBoards = self.canJump(newB, moveThisKing, X, Y, player, 'sw', opponents, allKings, newBoards, oldChinook)

	    #Move SouthEast (SE)?
	    if (X != 5 and Y != 5):
		if not( (self.Board[X+1][Y+1])[1] == moveThisKing.who):
		    newB = self.copyCTOR()
		    
		    newBoards = self.canJump(newB, moveThisKing, X, Y, player, 'se', opponents, allKings, newBoards, oldChinook)

	return newBoards #return all children boards given board
    #===================================================== 