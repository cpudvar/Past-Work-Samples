/*----------------------------------------------------------------------
Programmer: Caleb Pudvar & Andrew Thomas

Summary: This program was made to explore differences in memory management
         algorithms. For contiguous and segmented methods of memory input,
         both first fit and worst fit are implemented. A total of 4 files
         are supplied, each of which showcases the strength of one memory
         input formula over the other. There is a constant output
         which analyzes the location of various processes in memory, and
         accounts for fragmentation when necessary.
         
 
------------------------------------------------------------------------*/       

/*----------------------------------------------------------------------
INPUT:   One of the following hard-coded files.

         Options are:
            - "con_first.txt"
            - "con_worst.txt"
            - "seg_first.txt"
            - "seg_worst.txt"           
           

OUTPUT:     
         For each ADD or REMOVE in both Contiguous and Segmented versions,
         the following is displayed:

         ----------------------------
         ID: Pa      Memory: (Size)a
         ID: Pb      Memory: (Size)b
         ID: Pc      Memory: (Size)c
         .             .
         .             .
         .             .
         ID: Pend     Memory: (Size)end

         Total     Used     Free
           X         Y        Z

         ---------------------------- 
         
         Where:
                 -P denotes each process's ID (in the segmented section
                  each segment will be listed separately)
                  
                 -In the case that there is a free section, the ID will
                  be labeled FREE, followed by the size of the free space
                  
                 -X is total memory space (Kilobytes)
                     In our code, this is consistently 256,000 Kilobytes (256 MB)
                  
                 -Y is the total amount of used memory space (Kilobytes)
                      (not free)
                
                 -Z is the total amount of free space (Kilobytes)
                     (including freed fragments)
     
------------------------------------------------------------------------*/

import java.io.*;
import java.util.*;

//Class Management
public class Management {
	//Global Declarations
	//Max size of memory
	final static int MAX_SIZE = 256000;
	//Available space left
	static int availableSpace = MAX_SIZE;
	//List of Processes
	static LinkedList <Process> memory = new LinkedList<Process>();
	
	//MAIN
	public static void main(String [] args){
		//Declare scanners
		Scanner sc1 = null;
		Scanner sc2 = null;
		Scanner sc3 = null;
		Scanner sc4 = null;

		try {
			//File options (Choose one to run)
			File file = new File("con_first.txt");
			//File file = new File("con_worst.txt");
			//File file = new File("seg_first.txt");
			//File file = new File("seg_worst.txt");
			
			//Point scanners to file
			sc1 = new Scanner(file);
			sc2 = new Scanner(file);
			sc3 = new Scanner(file);
			sc4 = new Scanner(file);

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		//---------------------
		//Contiguous First Fit
		System.out.println("**********************");
		System.out.println("Contiguous - First Fit");
		System.out.println("**********************");
		//LOOP until file ends
		while (sc1.hasNextLine()) {
			Scanner s1 = new Scanner(sc1.nextLine());
			//LOOP until end of line
			while (s1.hasNext()) {
				String s = s1.next();
				//If starting process
				if (s.equals("S")){
					//Get name and size
					String name = s1.next();
					int space = Integer.parseInt(s1.next());
					contiguousProcess_First(name, space);
					printMemory();
					continue;
				}
				//If ending process
				if (s.equals("E")){
					//End it
					end_process(s1.next());
					//Combine free space then print
					combine_space();
					printMemory();
					continue;
				}
			}
		}
		//Close file and clear memory of FREE blocks
		sc1.close();
		memory.clear();
		
		//---------------------
		//Segmented First Fit
		System.out.println("\n\n**********************");
		System.out.println("Segmentation - First Fit");
		System.out.println("**********************\n");
		//LOOP until file ends
		while (sc2.hasNextLine()) {
			Scanner s2 = new Scanner(sc2.nextLine());
			//LOOP until end of line
			while (s2.hasNext()) {
				String s = s2.next();
				//If starting process
				if (s.equals("S")){
					//Get name and space needed
					String name = s2.next();
					int space = Integer.parseInt(s2.next());
					//Start process
					segmentedProcess_First(name, space, s2);
					printMemory();
					continue;
				}
				//If ending process
				if (s.equals("E")){
					//End it
					end_process(s2.next());
					//Combine free space, then print
					combine_space();
					printMemory();
					continue;
				}
			}
		}
		//Close file and clear memory of FREE blocks
		memory.clear();
		sc2.close();

		//---------------------
		//Contiguous Worst Fit
		System.out.println("**********************");
		System.out.println("Contiguous - Worst Fit");
		System.out.println("**********************");
		//LOOP until file ends
		while (sc3.hasNextLine()) {
			Scanner s3 = new Scanner(sc3.nextLine());
			//LOOP until line ends
			while (s3.hasNext()) {
				String s = s3.next();
				//If starting process
				if (s.equals("S")){
					//Get name and size
					String name = s3.next();
					int space = Integer.parseInt(s3.next());
					//Start process
					contiguousProcess_Worst(name, space);
					printMemory();
					continue;
				}
				//If ending process
				if (s.equals("E")){
					//End it
					end_process(s3.next());
					//Combine free space, then print
					combine_space();
					printMemory();
					continue;
				}
			}
		}
		//Close file and clear memory of FREE blocks
		sc3.close();
		memory.clear();

		//---------------------
		//Segmented Worst Fit
		System.out.println("\n\n**********************");
		System.out.println("Segmentation - Worst Fit");
		System.out.println("**********************\n");
		//LOOP until file ends
		while (sc4.hasNextLine()) {
			Scanner s4 = new Scanner(sc4.nextLine());
			//LOOP until line ends
			while (s4.hasNext()) {
				String s = s4.next();
				//If starting new process
				if (s.equals("S")){
					//Get name and size
					String name = s4.next();
					int space = Integer.parseInt(s4.next());
					//Start process
					segmentedProcess_Worst(name, space, s4);
					printMemory();
					continue;
				}
				//If ending process
				if (s.equals("E")){
					//End it
					end_process(s4.next());
					//Combine free space, then print
					combine_space();
					printMemory();
					continue;
				}
			}
		}
		//Close file and clear memory of FREE blocks
		memory.clear();
		sc4.close();
	}

	//Starts process for contiguous first fit
	private static void contiguousProcess_First(String name, int space) {
		//Space check
		if(availableSpace - space >= 0){
			availableSpace = availableSpace - space;
			Process compareID;
			//Search entire memory list
			for (int i = 0; i < memory.size(); i++){
				//Get each element
				compareID = memory.get(i);
				//If space is free, try to fit
				if (compareID.ID.equals("FREE")){
					//if space is less than free block then split
					if (compareID.size > space){
						memory.set(i, new Process(name, space));
						memory.add(i+1, new Process("FREE", (compareID.size - space)));
						return;
					}
					//If space is equal to free block then just put it in there
					else if (compareID.size == space){
						memory.set(i, new Process(name, space));
						return;
					}
					//Else it is not large enough and check for next block
					else{
						continue;
					}
				}
			}
			//If it cannot be fit then put it at end
			memory.add(new Process(name, space));
		}
		else{
			System.err.println("ERROR: MEMORY LIMIT EXCEEDED");
		}

	}

	//Starts process for Segmented First Fit
	private static void segmentedProcess_First(String name, int space, Scanner s2) {
		//Space check
		if(availableSpace - space >= 0){
			availableSpace = availableSpace - space;
			Process compareID;
			boolean replaced;
			//LOOP until end of line
			while (s2.hasNext()){
				//Get next segment size
				int part = Integer.parseInt(s2.next());
				//Bool to check if word was replaced
				replaced = false;
				// LOOP until word is replaced
				while (replaced == false){
					//Search entire memory
					for (int i = 0; i < memory.size(); i++){
						compareID = memory.get(i);
						//If free space is found then try and replace
						if (compareID.ID.equals("FREE")){
							//If size of space is larger than segment then add and shift everything
							if (compareID.size > part){
								memory.set(i, new Process(name, part));
								memory.add(i+1, new Process("FREE", (compareID.size - part)));
								//Word is replaced so break
								replaced = true;
								break;
							}
							//If segment size is same as free space then replace and do not shift
							else if (compareID.size == part){
								memory.set(i, new Process(name, part));
								//Change bool and break
								replaced = true;
								break;
							}
							else{
								//Keep looking if it doesn't fit
								continue;
							}
						}
					}
					//Check to see if replaced
					if (replaced == true){
						break;
					}
					//If nothing gets replaced then make new memory
					else{
						memory.add(new Process(name, part));
						replaced = true;
					}
				}


			}
		}			
		else{
			System.err.println("ERROR: MEMORY LIMIT EXCEEDED");
		}
	}
	
	//Start Contiguous Worst Fit
	private static void contiguousProcess_Worst(String name, int space) {
		//Space check
		if(availableSpace - space >= 0){
			availableSpace = availableSpace - space;
			int index = find_largest();
			Process compare;
			//If there are no free spaces then make new one
			if (index == -1){
				memory.add(new Process(name, space));
				return;
			}
			compare = memory.get(index);
			//If size of free memory is larger than process then split and shift
			if (compare.size > space){
				memory.set(index, new Process(name, space));
				memory.add(index+1, new Process("FREE", (compare.size - space)));
				return;
			}
			//If space fits exactly then replace
			else if (compare.size == space){
				memory.set(index, new Process(name, space));
				return;
			}
			//Else add new process if space is too small
			else if (compare.size < space){
				memory.add(new Process(name,space));
				return;
			}
		}
	}
	
	//Start Segmented Worst Fit
	private static void segmentedProcess_Worst(String name, int space,
			Scanner s4) {
		//Space check
		if(availableSpace - space >= 0){
			availableSpace = availableSpace - space;
			//LOOP until end of line
			while (s4.hasNext()){
				//Get segment space
				int part = Integer.parseInt(s4.next());
				//Find largest free space
				int index = find_largest();
				Process compare;
				//If there is no free space then add to end and move on
				if (index == -1){
					memory.add(new Process(name, part));
					continue;
				}
				compare = memory.get(index);
				//If segment is smaller than free space split and shift
				if (compare.size > part){
					memory.set(index, new Process(name, part));
					memory.add(index+1, new Process("FREE", (compare.size - part)));
					continue;
				}
				//If size of segment and free space is equal then replace
				else if (compare.size == part){
					memory.set(index, new Process(name, part));
					continue;
				}
				//Else it doesn't fit, add to end
				else if (compare.size < part){
					memory.add(new Process(name,part));
					continue;
				}
			}
		}
	}
	
	//Ends all processes with the same ID as passed
	private static void end_process(String next) {
		//Search entire memory
		for (int i = 0; i < memory.size(); i++){
			Process compare = memory.get(i);
			//Free the space if the ID matches
			if (next.equals(compare.ID)){
				memory.set(i, new Process("FREE", compare.size));
				availableSpace = availableSpace + compare.size;
				//Reset for loop to check again
				//i gets incremented to 0
				i = -1;
			}
		}
	}

	//Find largest value in list, returns index of that one
	private static int find_largest() {
		int index = -1;
		Process find;
		int largest = 0;
		//Search entire memory list
		for (int i = 0; i < memory.size(); i++){
			find = memory.get(i);
			//If it's a free block and larger than old largest then it becomes newest largest
			if (find.ID.equals("FREE")){
				if (find.size > largest){
					index = i;
					largest = find.size;
				}
			}
		}
		//Return index, if -1 then are free
		return index;
	}

	//Combine free space in memory
	private static void combine_space() {
		Process rep;
		Process check;
		//Search entire memory
		for (int i = 0; i < memory.size(); i++){
			rep = memory.get(i);
			//If a block is free
			if (rep.ID.equals("FREE")){
				//If end of memory then break
				if (memory.size() == i+1){
					break;
				}
				//Otherwise if next block is FREE then combine
				check = memory.get(i+1);
				if (check.ID.equals("FREE")){
					memory.remove(i+1);
					memory.set(i, new Process("FREE", (rep.size+check.size)));
					//Reset for loop to check again
					i = -1;
				}
			}
		}

	}
	
	//Prints memory
	public static void printMemory(){
		Process print;
		//Gets all processes from list and prints name and size
		for (int i = 0; i < memory.size(); i++){
			print = memory.get(i);
			System.out.printf("ID: %s %s \t Memory: %s\n", " ", print.ID, print.size);
		}
		//Prints total stats of what is used and what is free
		System.out.println("\nTotal\t Used\t Free");
		System.out.printf("%s\t %s\t %s\n\n", MAX_SIZE, (MAX_SIZE-availableSpace), availableSpace);
		System.out.println("-------------------------------");
	}
}