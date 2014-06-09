public class Fork {
	private boolean isAvailable;			//Bool: represents current state of fork (taken or free)	
	
	public synchronized void takeFork() throws InterruptedException {
		while (!isAvailable){
			wait();							//if currently desired fork is possessed by another Philosopher, 								
		}									//wait until that Philosopher relinquishes fork
		isAvailable = false;				//fork is in use
	}
	
	public boolean isForkAvailable(){
		return isAvailable;					//return true/false whether or not fork is held by a Philosopher
	}

	public Fork(boolean isAvailable) {		//Fork constructor, receives bool isAvailable
		this.isAvailable = isAvailable;
	}

	public synchronized void returnFork() { //Method to return fork when Philosopher has eaten
		isAvailable = true;
		notifyAll();						//Notify any Philosopher waiting on fork that it has been relinquished
	}
}

