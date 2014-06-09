/*----------------------------------------------------------------------
Programmer: Caleb Pudvar
 
Summary: This program is a concurrent simulation of the well-known 
		"Dining Philosopher's Problem" articulated by Dijkstra where 
		 n philosophers are sitting at a table with n forks placed 
		 between each member. Two forks are required to eat and at 
		 any time, a philosopher can only pick up one fork. Philosophers
		 transition through three states: thinking, hungry, and eating.
		 A philosopher may die if stays hungry for longer than half
		 of the maximum waiting time.		  

------------------------------------------------------------------------*/          
     
/*----------------------------------------------------------------------
INPUT: 	NONE
 
OUTPUT: For each iteration of a thread:
	 * Total time running: x milliseconds. (if desired)
	 * Total time thinking: x milliseconds.
	 * Total time being hungry: x milliseconds.
	 * Total time eating: x milliseconds
	 * Total number of starved Philosophers: x.
	 * 
	 * Mean thinking: x ms.
	 * Mean time being hungry: x ms.
	 * Mean time eating: x ms.
------------------------------------------------------------------------*/

public class Table {	
	static int totalPhilosophers = 5;		//Total number of philosophers desired
	
	public static int getTotalPhilosophers() {
		return totalPhilosophers;			//Returns total number of philosophers
	}
	public static void main(String args[]) {
		
		System.out.println("Running simulation for: " + totalPhilosophers + " philosophers.\n");
		Fork left = null, right = null;		//Initialize left and right fork, set to null temporarily
		Philosopher[] philosophers = new Philosopher[totalPhilosophers];	//create array of Philosopher objects, one for each philosopher
		Fork[] forks = new Fork[totalPhilosophers];							//creates array of Fork objects, same length as number of philosophers
		
		for(int i = 0; i < totalPhilosophers; i++){
			forks[i] = new Fork(true);				//set each fork initially to unused
		}
		
		for (int i = 0; i < totalPhilosophers; i++) {			
			if (i == 0) {							//declare left and right forks for first philosopher
				right = forks[i];					
				left = forks[totalPhilosophers-1];
			}
			if (i > 0) {							//declare left and right forks for subsequent philosophers
				right = forks[i];
				left = forks[i-1];
			}
			
			philosophers[i] = new Philosopher(i, totalPhilosophers, left, right, 0); //designate each block in philosophers[] with proper thread info (phil. #, total phil's, left fork, right fork, initial hungriness (should be zero)
			Thread thread = new Thread(philosophers[i]);							 //initialize thread of philosopher
			thread.start();															 //start thread (implicitly calls run() in Philosopher class
		}
	}
}