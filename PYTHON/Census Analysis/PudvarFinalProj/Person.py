#Person.py

from collections import Counter
import sets
import string

class Person(object):
    totalPeople = 0 #count of total words across corpus
    trainingPeople = 0
    testPeople = 0
    allPeople = [] #list of all people objects
    
#=====================================================    
    def __init__(self):
	"""CTOR"""
	self.train = None
	self.test = None
	self.use = True
	
	self.age = None                    #age 
	self.workClass = None              #working class
	self.fnlwgt = None                 #sampling weight
	self.education = None              #education
	self.educationNum = None           #education value
	self.maritalStatus = None	   #marital status
	self.occupation = None             #occupation
	self.familyRelationship = None     #relationship
	self.race = None                   #race
	self.sex = None                    #sex
	self.capitalGain = None            #capital gain
	self.capitalLoss = None            #capital loss
	self.hoursPerWeek = 0              #hours worked per week
	self.nativeCountry = None          #native country	    
	self.salary = None                 #salary of person
	
	self.cluster = []
	self.masterAttributes = []

	    
#=====================================================  

    def describePerson(self, attributes):
	self.age = attributes[0]
	self.workClass = attributes[1]            #not use
	self.fnlwgt = attributes[2]               #not use
	self.education = attributes[3]            #not use
	self.educationNum = attributes[4]
	self.maritalStatus = attributes[5]
	self.occupation = attributes[6]           #not use
	self.familyRelationship = attributes[7]   #not use
	self.race = attributes[8]
	self.sex = attributes[9]
	self.capitalGain = attributes[10]
	self.capitalLoss = attributes[11]
	self.hoursPerWeek = attributes[12]
	self.nativeCountry = attributes[13]
	self.salary = attributes[14]
	self.cluster = attributes
	    
#===================================================== 
    def getMasterValues(self):
	
	if(self.maritalStatus == ' married-civ-spouse'):
	    self.maritalStatus = 1    # person married, or not
	else:
	    self.maritalStatus = 0
	    
	if(self.nativeCountry == ' united-states'):  #is person from united states, or not
	    self.nativeCountry = 1
	else: 
	    self.nativeCountry = 0
	  
	if(self.race == ' white'):          #is person white? or other
	    self.race = 1
	else:
	    self.race = 0
	    
	if(self.sex == ' male'):   #is person male or female?
	    self.sex = 1
	else:
	    self.sex = 2
	    
	self.masterAttributes.append(self.salary)
	self.masterAttributes.append(self.age)
	self.masterAttributes.append(self.educationNum)
	self.masterAttributes.append(self.maritalStatus)
	self.masterAttributes.append(self.race)
	self.masterAttributes.append(self.sex)
	self.masterAttributes.append(self.capitalGain)
	self.masterAttributes.append(self.capitalLoss)
	self.masterAttributes.append(self.hoursPerWeek)
	self.masterAttributes.append(self.nativeCountry)	
	    
    
#=====================================================