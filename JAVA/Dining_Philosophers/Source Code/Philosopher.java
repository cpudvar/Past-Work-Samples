import java.util.Random;		

public class Philosopher implements Runnable {	
	private Random random = new Random();		//new instance of Random
	private Fork left;							//left fork object, relates to current thread
	private Fork right;							//right fork object, relates to current thread
	@SuppressWarnings("unused")
	private int whichPhilosopher;				//which array location in philosophers[]
	private int numberOfPhilosophers;			//total number of philosophers, used for mean calculation
	private int maxRandom = 2000;				//max sleep time at any point (in ms) corresponds to 2 seconds
	private int numForks;						//represents number of forks philosopher is holding at any point
	private int randomWait = 0;					//time thread spends being hungry for rotation
	private int randomThink = 0;				//time thread spends thinking for rotation
	private int randomEat = 0;					//time thread spends eating for rotation
	private int tempHungry = 0;					//hungry time of round to compare to the max, see if thread starves
	
	private long totalBefore = 0;				//calculate total elapsed time
	private long totalAfter = 0;
	
	private long thinkBefore = 0;				//calculate total thinking time
	private long thinkAfter = 0;
	
	private long hungryBefore = 0;				//calculate total hungry time
	private long hungryAfter = 0;
	
	private long eatBefore = 0;					//calculate total eating time
	private long eatAfter = 0;
	
	private static long totalRunning = 0;		//total run time
	private static long totalThinking = 0;		//total thinking time
	private static long totalHungry = 0;		//total hungry time
	private static long totalEating = 0;		//total eating time
	private static int totalStarved = 0;		//number of total starved threads	
	

	/*Philosopher constructor: parameters (int, int, Fork, Fork, int)
	 * 
	 * Receives the following in order: (int)  current thread
	 * 									(int)  total number of threads
	 * 									(Fork) left fork status of current thread
	 * 									(Fork) right fork status of current thread
	 * 									(int)  hungriness of current thread 
	 */		
	public Philosopher(int whichPhilosopher, int numberOfPhilosophers, Fork left, Fork right, int tempHungry) {
		this.whichPhilosopher = whichPhilosopher;
		this.numberOfPhilosophers = numberOfPhilosophers;
		this.left = left;
		this.right = right;
		this.numForks = 0;
		this.tempHungry = tempHungry;
	}	
	
	
	//access private member totalThinking
	public static long getTotalThinking() {
		return totalThinking;
	}

	//access private member totalHungry
	public static long getTotalHungry() {
		return totalHungry;
	}

	//access private member totalEating
	public static long getTotalEating() {
		return totalEating;
	}
	
	//access private member totalRunning
	public static long getTotalRunning() {
		return totalRunning;
	}

	//access private member totalStarved
	public static int getTotalStarved() {
		return totalStarved;
	}
	
	
	/*
	 * The following method simply displays information about the thread system, 
	 * and updates & displays as each thread is completed:
	 * 
	 * Total time running: x milliseconds. (if desired)
	 * Total time thinking: x milliseconds.
	 * Total time being hungry: x milliseconds.
	 * Total time eating: x milliseconds
	 * Total number of starved Philosophers: x.
	 * 
	 */
	public static void printStats(){
		//System.out.println("\nTotal time running: " + getTotalRunning() + " milliseconds.");
		System.out.println("Total time thinking: " + getTotalThinking() + " milliseconds.");
		System.out.println("Total time being hungry: " + getTotalHungry() + " milliseconds.");
		System.out.println("Total time eating: " + getTotalEating() + " milliseconds.");
		System.out.println("Number of starved Philosophers: " + getTotalStarved() + ".\n");
	}
	
	
	/*
	 * The following method uses the necessary running totals in order to calculate 
	 * a mean value for thinking, hungry, and starved states:
	 * 
	 * Mean thinking: x ms.
	 * Mean time being hungry: x ms.
	 * Mean time eating: x ms.
	 * 
	 * These are the values that are used for each data point in the analysis	 * 
	 */
	public static void returnMeans(){
		float meanThinking = getTotalThinking()/Table.getTotalPhilosophers();		//total thinking / total philosophers
		float meanHungry = getTotalHungry()/Table.getTotalPhilosophers();			//total hungry / total philosophers
		float meanEating = getTotalEating()/Table.getTotalPhilosophers();			//total eating / total philosophers
		
		System.out.println("Mean thinking: " + meanThinking + " ms.");
		System.out.println("Mean time being hungry: " + meanHungry + " ms.");
		System.out.println("Mean time eating: " + meanEating + " ms.");
	}
	
	//Execution path of each thread
	public void run() {
		try {
			randomWait = random.nextInt(maxRandom);							//decide time to wait after philosopher picks up fork (max 2000ms)
			randomThink = random.nextInt(maxRandom);						//decide time to wait for philosopher to think on rotation (max 2000ms)
			randomEat = random.nextInt(maxRandom);							//decide time philosopher will spend eating on rotation (max 2000ms)
			
			int hungryCheck = maxRandom/2;									//determines max time thread can be hungry without starving
			
			for (int i = 0; i < numberOfPhilosophers; i++) {				
				totalBefore = System.currentTimeMillis();					//initialize total elapsed time counter

				if ( numForks == 0 ) {										//if thread has no forks
					thinkBefore = System.currentTimeMillis();				//begins thinking
					Thread.sleep(randomThink);
					//System.out.println("Philosopher " + whichPhilosopher + " is thinking.");
					thinkAfter = System.currentTimeMillis();				//stops thinking
					totalThinking = totalThinking + thinkAfter - thinkBefore;//calculate total elapsed thinking time for system
				}
				
				//System.out.println("Philosopher " + whichPhilosopher + " is hungry.");
				hungryBefore = System.currentTimeMillis();					//begins being hungry
				
				
				//NOTE: thread may only take one fork at a time.
				//		must hold and return to acquire both forks
				if (right.isForkAvailable()) {								//right fork available?
					right.takeFork();										//takes fork
					//System.out.println("Philosopher " + whichPhilosopher + " grabbed right fork.");
					numForks++;												//thread has another fork
					Thread.sleep(randomWait);
					totalHungry = totalHungry + randomWait;					//thread waits, gets hungry
					
				}else if (left.isForkAvailable()) {							//left fork available?
					left.takeFork();										//take it
					//System.out.println("Philosopher " + whichPhilosopher + " grabbed left fork.");
					numForks++;												//thread has another fork
					Thread.sleep(randomWait);
					totalHungry = totalHungry + randomWait;					//thread waits, gets hungry
				} 
				
				if(tempHungry > hungryCheck){								//thread been hungry too long?
					tempHungry = 0;											//reset hungriness
					numForks = 0;											//if yes, release both forks	
					right.returnFork();		
					left.returnFork();
					totalStarved++;											//thread starves :(
					Thread.currentThread().interrupt();						//terminate thread
				}
				else if ( numForks == 2 ) {									//thread has both forks and can eat
					//System.out.println("Philosopher " + whichPhilosopher + " is eating food.");
					hungryAfter = System.currentTimeMillis();				//thread isn't hungry any more
					totalHungry = totalHungry + hungryAfter - hungryBefore; //calculate total hungriness for all threads
					
					eatBefore = System.currentTimeMillis();					//start eating
					Thread.sleep(randomEat);	
					eatAfter = System.currentTimeMillis();					//stop eating
					
					totalEating = totalEating + eatAfter - eatBefore;		//calculate total eating time for all threads
					left.returnFork();										//done eating, return forks
					right.returnFork();
					numForks = 0;
					tempHungry = 0;											//not hungry any more
					//System.out.println("Philosopher " + whichPhilosopher + " put forks back and is done eating.");	
				} 
				else {
					//System.out.println("Philosopher " + whichPhilosopher + " is waiting to have two forks.");
					Thread.sleep(randomWait);	
					tempHungry = tempHungry + randomWait;					//thread still has one fork, couldn't grab another but hasn't starved
				}				
				totalAfter = System.currentTimeMillis();					//stop tallying total
				totalRunning = totalRunning + totalAfter - totalBefore;		//total run time up to current thread (acts as if system was run linearly
				
			}
		} catch (InterruptedException e) {
			//A thread has starved, total starved incremented
		}
		
		printStats();														//display stats from initialization until end of current thread
		returnMeans();														//display averages from initialization until end of current thread (final display is accurate)
	}	
}