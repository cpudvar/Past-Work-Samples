"""
Programmer: Caleb Pudvar
    For information & statistics about program, 
    please refer to the readme and accompanying report
"""

from Manhattan_BoardClass import *
import queue
import time

# implemented in Python v3.1.2

#=====================================================  

def main():
        timesToRun = 100
	
	#initialize timer
        start = time.time()
	
	#execute program
        totalNumberOfMoves, allMaxQs = execute(timesToRun)

        print("\nHEURISTIC: Manhattan Distance")
        print("\nAverage Number of moves: ", totalNumberOfMoves / timesToRun)
        print("Average Max Queue Size: ", allMaxQs / timesToRun)
	
        #calculates elapsed program run-time
        elapsed = time.time() - start
	
        print("\nTotal runtime: ", str(elapsed) + " seconds.") 
        print("Average runtime: ", str(elapsed/timesToRun) + " seconds.")
	
#=====================================================

def execute(iterations):
        """INPUT: number of times to run
	   OUTPUT: total number of moves, sum of all max queue lengths for each execution
	   
	   Description: given a number of times to run, this will run best-first search 
	   on a randomly generated board and return the total moves and total queue length
        """	
        movesTotal = 0
        maxQTotal = 0

        """run for given amount of iterations"""
        for execution in range(0, iterations):
                b = BoardClass()
                """generate the board"""
                b.initializePuzzleBoard()
        
                """run Best-First Search on board
		   returns number of moves to solve and max queue length
                """
                numMoves, maxQ = BestFirstSearch(b)
		
                """keep track of the total over the given execution period"""
                movesTotal += numMoves
                maxQTotal += maxQ

        return movesTotal, maxQTotal

#=====================================================

def FindSolutionPath(board):
        """INPUT: board
	   OUTPUT: list containing solution path
	   
	   Description: given a board (that is a solution), backtraces parents
	   until the solution path is found. this path is returned
        """
        solutionPath = []
	
        """while the board has a parent(isnt root), add board to the list"""
        while (board.Parent):
                parentBoard = board.Parent
                solutionPath.append(board)
                board = parentBoard
		
        """loop stops when root reached, so add root"""
        solutionPath.append(board)
	
        """reverse list order so root is first"""
        solutionPath.reverse()
        return solutionPath

#=====================================================	

def BestFirstSearch(startingBoard):
        """INPUT: starting board
	   OUTPUT: number of moves, max queue length
	   
	   Description: given a board this best first search algorithm uses a 
	   priority queue to keep track of the best available board using a desired 
	   heuristic. When a solution is found, the number of moves and queue length 
	   are returned for analysis. 
	   
	   Code to display the solution path has been inactivated. Instructions to view solution
	   path are below.
        """
	 
        maxQ = 0
	
        """implement priority queue
           boards are added as (heuristic value of board, board)	   
        """
        Q = queue.PriorityQueue()
	
        """add starting board and heuristic to queue"""
        Q.put( (startingBoard.ManhattanDistance, startingBoard) )
	
        moves = 0
	
        Visited = []
        Solution = []
	
        """ if starting with a goal board, exit """
        if(startingBoard.isGoal()):
                print("You're starting with a solved board!")
                return 0, 0
        
        """as long as queue has a board, continue"""
        while not Q.empty():
		
                """keep track of max queue length"""
                if(int(Q.qsize()) > maxQ):
                        maxQ = Q.qsize()
			
                """grab board with best heuristic value"""
                bestBoard = Q.get()

                Visited.append(bestBoard[1])

                """if next board is the goal, find solution"""
                if(bestBoard[1].isGoal()):
                       
                        #print("\nFINAL PATH ")
                        
                        """from goal board, backtrace through parents to find goal path"""
                        solution = FindSolutionPath(bestBoard[1])    
			
                        for board in solution:
                                """To see the goal path of solved board,
				   uncomment the green code within this loop
                                """
                                #if(moves == 0):
                                #        print("\nStarting board:")
                                #else:
                                #        print("Move #", moves)
                                #print(board)
                                moves+=1
                        
                        return moves-1, maxQ
		
                """create children of current best board"""
                children = bestBoard[1].createChildrenBoards()

                """add unvisited children boards to visited list based on heuristic"""
                for board in children:
                        if(board not in Visited):
                                board.computeManhattan()
                                Q.put( (board.ManhattanDistance, board) )
        
	# should never reach this code
        print ("No Solution ... ???")
        
        return -1, -1

#===================================================== 

#===========\
# START HERE \
#===================================================== 	
if __name__ == '__main__':
        main()

#===================================================== 
