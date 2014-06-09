
""" Class for instances of 8-puzzle Boards """

import random
import string

class BoardClass(object):
    """NxN board to solve [(N^2)-1]-puzzle"""
    
    # class members (all instances use this same values)    
    N = 3
    
    GOAL  = [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]    
    	
    #=====================================================  
    
    def __init__(self):
        """CTOR
        """
	# setup board (set bogus values)
        self.Board = [ [-1, -1, -1], [-1, -1, -1], [-1, -1, -1] ]

	# (X,Y) = current location of the EMPTY TILE (0)
        self.X = -1   # ROW
        self.Y = -1   # COL
	
	# root
        self.Parent = False
	
        """invalid value initializing heuristic"""
        self.tilesToGoal = -1	
	
    #===================================================== 
    
    def copyCTOR(self):
        """Copy CTOR: replicates every attribute of the provided board 
		      and returns that board
        """
        newBoard = BoardClass()
        newBoard.Board = []
        for nextRow in self.Board:
            newRow = []
            for nextTile in nextRow:
                newRow.append(nextTile)
            newBoard.Board.append(newRow)
        newBoard.X = self.X
        newBoard.Y = self.Y
        newBoard.Parent = self.Parent
	
        newBoard.tilesToGoal = self.tilesToGoal	
	
        return newBoard
    
    #=====================================================
    
    def possibleBoard(self, tiles):
        """INPUT: randomly arranged list of values 0-8 inclusive
	   OUTPUT: boolean True if board is solvable, False if not
	   
	   Description: after generating a random list, this determines
			if it will correlate to a possible 8-puzzle board
        """
        inversions = 0
	
        """for each tile in the list"""
        for index1 in range(0, len(tiles)):
            """look ahead to all tiles to the right of it"""
            for index2 in range(index1+1, len(tiles)):
                """inversion found when tile (not 0) is greater than a tile following it"""
                if(tiles[index1] != 0) and (tiles[index2] != 0) and (tiles[index1] > tiles[index2]):
                    inversions+=1
        """board is possible if inversions is even"""
        if(inversions%2==0):
            return True
        else:
            return False
	
    #===================================================== 
    
    def findBlankSpace(self):
        """INPUT: none
	   OUTPUT: none
	   
	   Description: locates the blank space after generating a random board,
	   setting the X and Y coords of space as board attribute
        """
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                if(self.Board[row][col] == 0):
                    self.X = row
                    self.Y = col
		    
    #===================================================== 
    
    def findGoalTile(tile):
        """INPUT: value of a single tile
	   OUTPUT: the row and col of desired tile
	   
	   Description: for the goal board, locates the row and col values of the tile
        """
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                if(BoardClass.GOAL[row][col] == tile):
                    return row, col
		    
    #===================================================== 
    
    def findBoardTile(self, tile):
        """INPUT: value of a single tile
	   OUTPUT: the row and col of desired tile
	   
	   Description: for a given board, locates the row and col values of the tile 
        """
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                if(self.Board[row][col] == tile):
                    return row, col
		    
    #===================================================== 		    
    def initializePuzzleBoard(self):
        """INPUT: NONE
	   OUTPUT: NONE
	   
	   Description: Set actual (row,col) locations for each tile in the GOAL board
	   and initialize the starting board
        """
		
        """Starting board set up""" 
	
        tiles = [0,1,2,3,4,5,6,7,8]
	
        """randomly arrange the contents of tiles[]"""
        random.shuffle(tiles)                            
	
        """keep shuffling list around until a possible board is found"""
        while(self.possibleBoard(tiles) == False):
            random.shuffle(tiles)
            self.possibleBoard(tiles)
	
        """arrange the list into a board"""
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                self.Board[row][col] = tiles.pop(0)
	
        """find the blank space in random board"""
        self.findBlankSpace()		
	
	#easy (4 moves)
        """uncomment the 3 lines below to override the random 
	   board with a simple one
	"""
        #self.Board = [ [3, 1, 2], [4, 7, 5], [6, 8, 0] ]
        #self.X = 2
        #self.Y = 2
	
        #medium (7 moves)
        """uncomment the 3 lines below to override the random 
	   board with a fairly simple one
	"""
        #self.Board = [ [3, 2, 5], [4, 1, 8], [6, 0, 7] ]
        #self.X = 2
        #self.Y = 1
	
        """will not pass unless the blank space is known"""
        assert ( self.Board[self.X][self.Y] == 0 )
	
        """compute heuristic values for starting board"""

        self.computeTilesToGo()
	
    #===================================================== 
    
    def createChildrenBoards(self):
        """ INPUT: a board
	    OUTPUT: list of possible children boards
	    
	    Description: Creates the set of potential children 
	    boards from the current board 
        """
        row = self.X
        col = self.Y
	
        assert( (row >=0 and row < BoardClass.N)
                and
                (col >=0 and col < BoardClass.N) )
	        
        newChildrenBoards = []
	
        
        """ FOR ALL POSSIBLE CHILD BOARDS
        	
	if empty tile can be moved:
	    1. a copy of the original is made
	    2. the two tiles are switched to move the blank
	    3. X or Y coords are changed to keep blank location intact
	    4. the parent is remembered
	    5. board is added to the list of all children
        """
	# UP(NORTH): slide empty (0) space up
        if ( row != 0 ):
	    
            northCopy = self.copyCTOR()
            northCopy.Board[row][col], northCopy.Board[row - 1][col] = northCopy.Board[row - 1][col], northCopy.Board[row][col]
            northCopy.X = row - 1
            northCopy.Parent = self
            newChildrenBoards.append(northCopy)
            
	# RIGHT(EAST): slide empty (0) space to right
        if ( col != (self.N - 1) ):
	    
            eastCopy = self.copyCTOR()	    
            eastCopy.Board[row][col], eastCopy.Board[row][col+1] = eastCopy.Board[row][col+1], eastCopy.Board[row][col]
            eastCopy.Y = col+1	    
            eastCopy.Parent = self
            newChildrenBoards.append(eastCopy)
	
	# DOWN(SOUTH): slide empty (0) space down
        if ( row != (self.N - 1) ):
	    
            southCopy = self.copyCTOR()
            southCopy.Board[row][col], southCopy.Board[row + 1][col] = southCopy.Board[row + 1][col], southCopy.Board[row][col]
            southCopy.X = row + 1
            southCopy.Parent = self
            newChildrenBoards.append(southCopy)
	    
	# LEFT(WEST): slide empty (0) space to left
        if ( col != 0 ):

            westCopy = self.copyCTOR()	    
            westCopy.Board[row][col], westCopy.Board[row][col-1] = westCopy.Board[row][col-1], westCopy.Board[row][col]
            westCopy.Y = col - 1
            westCopy.Parent = self
            newChildrenBoards.append(westCopy)
	    
        """ returns the list of children boards"""
        return newChildrenBoards
    
    #=====================================================
    
    def isGoal(self):
        """INPUT: board
	   OUTPUT: true if board is goal, false otherwise
	   
	   Description: given a board, the following code determines
	   if the goal has been reached
        """
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                if(BoardClass.GOAL[row][col] != self.Board[row][col]):
                    return False
        else:
            return True
    
    #=====================================================
    
    def computeTilesToGo(self):
        """INPUT: board
	   OUTPUT: # of correct tiles in board assigned to that board
	   
	   Description: given a board, this code calculates the
	   number of correct tiles in that board. Because of how a 
	   priority queue operates, this heuristic must be inverted to place
	   better boards on the front of the queue
        """
	
        right = 0                  #assume worst

        """find number of right tiles"""
        for row in range(0, self.N):
            for col in range(0, self.N):
                if(BoardClass.GOAL[row][col] == self.Board[row][col]):
                    right+=1

        """because of auto-ordering of priority queue, better boards need the smallest value"""	
        numTiles = self.N**2
        self.tilesToGoal = numTiles - right
	
    #=====================================================
    
    def __str__(self):
        """ Prints the current Board positions """
	
        print ("-------------")
        print ("| %d | %d | %d |" % (self.Board[0][0], self.Board[0][1], self.Board[0][2]))
        print ("-------------")
        print ("| %d | %d | %d |" % (self.Board[1][0], self.Board[1][1], self.Board[1][2]))
        print ("-------------")
        print ("| %d | %d | %d |" % (self.Board[2][0], self.Board[2][1], self.Board[2][2]) )
        print ("-------------")
        
        return ""
   
    #=====================================================         
    def __eq__(self, other):
        """INPUT: current board, another board
	   OUTPUT: True if boards are same, false otherwise
	   
	   Description: given two boards, this code checks each
	   corresponding value of them to determine if they are 
	   identical
        """
        for row in range(0, self.N):
            for col in range(0, self.N):
                if(self.Board[row][col] != other.Board[row][col]):
                    return False                    
        return True	
    
   #=====================================================         
    def __ne__(self, other):
        """INPUT: current board, another board
	   OUTPUT: True if boards are not identical, false otherwise
	   
	   Description: given two boards, this returns the result of __eq__
        """
	
        return (self == other)

    #=====================================================    
    
    def __lt__(self, other):
        """INPUT: current board, another board
	   OUTPUT: True if current board's heuristic is less than
	   other board, False otherwise
	   
	   Description: given two boards, the two heuristics are compared.
	   If the current board's heuristic is less than the other, this returns true
        """

        return (self.tilesToGoal < other.tilesToGoal)
        
    #===================================================== 
    
    def __le__(self, other):
        """INPUT: current board, another board
	   OUTPUT: True if current board's heuristic is less than
	   other board, False otherwise
	   
	   Description: given two boards, the two heuristics are compared.
	   If the current board's heuristic is less or equal to the other, this returns true
        """	

        return (self.tilesToGoal <= other.tilesToGoal)
        
    #=====================================================    