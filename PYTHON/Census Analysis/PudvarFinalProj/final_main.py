"""
Programmer: Caleb Pudvar
Description: See README for program information
"""
from Person import *
import glob
import os
import csv
import sys
def main():
        setup()
	createCARTFile()
	createMasterFile()
    
def setup(): 
	count  = 0
	inTest = 0
	inTrain = 0
	L = glob.glob('Data/*')
	for nextFile in L: #check each text file within Data
			
		text = open(nextFile, 'r')

		for line in text:
			newPerson = Person()       #new person object		

			if (nextFile == 'Data\\test.txt'):
				newPerson.test = True
				newPerson.train = False
				Person.testPeople += 1
			elif (nextFile == "Data\\training.txt"):
				newPerson.test = False
				newPerson.train = True
				Person.trainingPeople += 1
			else: 
				print 'test/train error'
				
			line = line.lower().rstrip()
			line = ''.join([char.strip('.') for char in line])
			if('?' in line): 
				newPerson.use = False
				count +=1
			
			attributes = line.split(',')
			
			newPerson.describePerson(attributes)
			if((newPerson.use == True) and ( newPerson.test == True)):
			        inTest +=1
			elif((newPerson.use == True) and (newPerson.train == True)):
			        inTrain +=1
			
			Person.totalPeople += 1
			
			Person.allPeople.append(newPerson) #add paper to list of paper objects
		text.close()
		
	check(count, inTest, inTrain)
    
#================================================================
def check(count, inTest, inTrain ):
	print "Total people: ", Person.totalPeople
	print "Number of people in test: ", inTest, Person.testPeople
	print "Number of people in training: ", inTrain, Person.trainingPeople
	print "Number of people not to use: ", count

#================================================================

def createCARTFile():
	"""
	INPUT: the set of preprocessed words
	OUTPUT: .CSV file for the set readable by CART
	"""	
	with open('CensusCART.csv', 'wb') as f:
		writer = csv.writer(f)
		columns = ['Income', 'Age', 'Education', 'Hours per Week']
		data = []
			
		writer.writerow(columns)
		for person in Person.allPeople:
			if(person.use):
				data.append(person.salary)            #salary as guiding attribute
				data.append(person.age)               #age
				data.append(person.educationNum)      #numerical representation of education
				data.append(person.hoursPerWeek)      #hours per week
	
				writer.writerow(data) #write list to .csv
			data = []

#================================================================


def createMasterFile():
	"""
	INPUT: the set of preprocessed words
	OUTPUT: .CSV file for the set readable by CART
	"""	
	with open('master.csv', 'wb') as f:
		writer = csv.writer(f)
		columns = ['Income', 'Age', 'Education', 'Marital Status', 'race', 'sex', 'Capital Gain', 'Capital Loss', 'Hours per Week', 'Native Country']
		data = []
			
		writer.writerow(columns)
		for person in Person.allPeople:
			person.getMasterValues()
			
			if(person.use):
				for value in person.masterAttributes:
					data.append(value)
	
				writer.writerow(data) #write list to .csv
			data = []			
#================================================================
			
if __name__ == '__main__':
	main()
# ===============================================================