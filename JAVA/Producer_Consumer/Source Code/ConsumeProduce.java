/*----------------------------------------------------------------------
Programmer: Caleb Pudvar
 
Summary: This program is a concurrent simulation of the Consumer/Producer
 		 problem. In this, a thread decrements some count as long as the
 		 count is greater than zero, whilst another thread increments as 
 		 long as the buffer isn't maxed out. There is only functionality 
 		 for one consumer and one producer. 
 		 
 		 For a clearer understanding, I built in a restaurant-style theme
		 where the consumer is a very hungry customer and the producer is
		 a waiter constantly bringing him food. The buffer consists of a 
		 plate that can hold up to X food.

------------------------------------------------------------------------*/          
     
/*----------------------------------------------------------------------
INPUT: 	NONE
 
OUTPUT:
 	 For each iteration of the producer thread:
 	 * "Delivering Meal #X"
 	 * "Total amount of food on plate: (food left)"
	 
	 For each iteration of the consumer thread:
 	 * "Total Meals Consumed: (total eaten)"
------------------------------------------------------------------------*/

import java.util.LinkedList;
import java.util.Queue;
import java.util.concurrent.*;

public class ConsumeProduce {

	Queue<Integer> food = new LinkedList<Integer>();
	int eaten = 0;												// stores amount of food customer has eaten
	final static int MAX_FOOD = 50;								// "buffer size" - size of queue
	final int MAX_CONSUME = 1000;								// controls program length; ends when consumer has consumed this amount of food

	public static void main(String args[]) {
		ConsumeProduce process = new ConsumeProduce();
		Consumer consumer  = process.new Consumer();	
		Thread waiter = new Thread(process.new Producer());		// declare producer thread		
		Thread customer = new Thread(consumer);					// declare consumer thread
		
		waiter.start();											// initialize producer
		
		customer.start();										// initialize consumer
		
		try {													// insert sleep section between thread initialization to allow
			Thread.sleep(50);									// producer to get a head start on consumer
		} catch (InterruptedException e) {}			
		
	}

	class Consumer implements Runnable {		

		public void run() {
			while (eaten < MAX_CONSUME) {						// while the consumption limit hasn't been reached...
				synchronized (food) {
					while (food.isEmpty()) {					// while there's not food to consume...
						try {
							food.wait(30);						// wait for more to arrive
						} catch (InterruptedException e) {
							Thread.interrupted();
						}
					}
					consume();									// call consume()
				}                            
			}
		}

		// no parameters
		public void consume() {
			if (!food.isEmpty()) {
				System.out.println("\nTotal Meals Consumed: " + food.remove());		// consume one element of food, also display the amount consumed so far
				eaten++;
			}
		}
	}

	class Producer implements Runnable {	

		public void produce(int i) {					
			food.add(new Integer(i));																				// add a new element to the food queue
			System.out.println("\nDelivering Meal #" + i + "\n Total amount of food on plate: " + food.size());		// displays total number served and
																													// amount currently on buffer
		}

		public void run() {
			int i = 1;			

			while (eaten < MAX_CONSUME ) {									// while the consumption limit hasn't been reached...
				synchronized (food) {
					while( (food.size() < MAX_FOOD)){						// as long as there's room on the plate
						try {
							food.wait(20);									// wait for more to arrive
						} catch (InterruptedException e) {
							Thread.interrupted();
						}
						if(eaten <= MAX_CONSUME){							// if the consumption limit hasn't been reached...
							produce(i);										// bring more food
							i++;
							food.notifyAll();								// let the consumer thread know there's food
						}					
					}
				}					
			}
		}		
	}
}