"""
Programmer: Caleb Pudvar
Description: See README for program information
"""
import re
import csv
import glob
import os
from Papers import *

def main():
	
	masterDict = setup()	#assemble dictionary of all words and their counts
	hamiltonSet = findAuthorWords('H') #all words hamilton uses
	madisonSet = findAuthorWords('M')  #all words madison uses
	jaySet = findAuthorWords('J')      #all words jay uses
	
	rawSet, rawFeatures = computeRawFeatures(hamiltonSet, madisonSet, jaySet, masterDict)
	computeRawDict(rawSet)
	preSet, preDict = computePreprocessed(rawSet, rawFeatures)
	computePreDict(preSet)
	
	createClusterFile(rawSet, 'Raw_Text.csv', 'raw')
	createClusterFile(preSet, 'Preprocessed_Text.csv', 'preprocessed')
	createCARTFile(preSet)

def setup():
	masterDictionary = Counter()
	removePunctuation = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~' #punctuation to remove
	nums = '1234567890'
	
	L = glob.glob('Federalist_Papers/*')
	for nextSubDir in L: #check each subdirectory within Federalist_Papers
		F = glob.glob(nextSubDir+'/*.txt') #finds all text files within subdirectories
		for nextFile in F:
			temp = ''
			newPaper = Papers()        #new paper object
			for char in nextFile:      #get paper number
				if char in nums:
					temp += ''.join(char)
			newPaper.number = temp
			
			authFetch = nextFile[::-1]
			newPaper.author = authFetch[4] #reverse path and index to receive author
			
			newPaper.path = 'FED_'+newPaper.number+'_'+newPaper.author+'.txt' 
			#build path name in acceptible format for cluster
			
			text = open(nextFile, 'r')

			for line in text:
				line = line.lower().rstrip()
				line = ''.join([char.strip(removePunctuation) for char in line])
				newPaper.text = line
				allWords = line.split()
				
				for word in allWords:
					Papers.totalWords += 1
					newPaper.paperDict[word] += 1
					newPaper.words += 1
					masterDictionary[word] += 1
					if(word not in newPaper.paperSet):
						newPaper.paperSet.add(word)
				
			Papers.allPapers.append(newPaper) #add paper to list of paper objects
			text.close()
	return masterDictionary #returns dictionary of all words and their counts

# ===============================================================

def getWordcloudWords():
	"""
	prints words (n) number of times to be copied 
	to generate word cloud
	"""
	for paper in Papers.allPapers:
		for word in paper.rawDict:
			if paper.rawDict[word] != 0:
				times = paper.rawDict[word]
				for i in range(times):
					print word
					
# ===============================================================
		
def findAuthorWords(author):
	"""
	Given an author, cycles through each text by that author.
	Adds new words to the set of words that author uses across
	all his/her works
	"""
	authorSet = set()
	for paper in Papers.allPapers:
		if(paper.author == author):
			authorSet = authorSet | paper.paperSet
	
	return authorSet

# ===============================================================

def computeRawFeatures(hamilton, madison, jay, master):
	
	rawFeatures = Counter()
	rawSet = (hamilton & madison & jay) 
	#build set of words that are only used by each author
	
	for word in master:
		if word in rawSet:
			rawFeatures[word] += master[word]
			#add word to rawFeatures if it is not present, increment otherwise
	return rawSet, rawFeatures	

# ===============================================================

def computePreprocessed(rawSet, rawFeatures):
	total = Papers.totalWords
	processedFeatures = Counter()
	processedSet = set()
	
	for word in rawSet:		
		if word in rawFeatures:
			relFreq = (float((rawFeatures[word]))/float(total)) * 100
			#find relative frequency of each word in a given paper
			if(relFreq >= Papers.meanFrequency):
				processedSet.add(word)
				processedFeatures[word] += relFreq
				#add word to processedFeatures if it is not present, increment otherwise
			
	return processedSet, processedFeatures	

# ===============================================================

def computeRawDict(rawSet):
	"""
	given the raw set of words, build a dictionary containing the counts
	of all appropriate words for each paper
	"""
	for paper in Papers.allPapers:
		for word in rawSet:
			paper.rawDict[word] += 0		
		
		for word in paper.paperDict:
			if word in rawSet:
				paper.rawDict[word] += paper.paperDict[word]	

#================================================================ 

def computePreDict(preSet):
	"""
	given the preprocessed set of words, build a dictionary containing the counts
	of all appropriate words for each paper
	"""	
	for paper in Papers.allPapers:
		for word in preSet:
			paper.preDict[word] += 0
		
		for word in paper.paperDict:
			if word in preSet:
				relFreq = (float((paper.paperDict[word]))/float(paper.words)) * 100
				relFreq = round(relFreq, 2)
				if(relFreq >= Papers.meanFrequency):
					paper.preDict[word] += relFreq
								
#================================================================

def createClusterFile(set, name, form):	
	"""
	INPUT: set, file name for output, form(either 'raw' or 'preprocessed')
	OUTPUT: .CSV file for the set readable by 2_ClusterFed.py (included)
	"""
	with open(name, 'wb') as f:
		writer = csv.writer(f)
		columns = []
		data = []
		columns.append('words')
		for paper in Papers.allPapers:
			columns.append(paper.path)	#generate list for file headers	
		
		writer.writerow(columns)
		for word in set: #for each word in the given set
			data.append(word) #add as first value of row in .csv
			for paper in Papers.allPapers:
				if form == 'raw':
					value = (float(paper.rawDict[word]))/(float(paper.words))
					data.append(value) #for each paper for given word, compute raw frequency 
				elif form == 'preprocessed':
					data.append(paper.preDict[word]) #add word's relative frequency
				else:
					print "shouldn't be here"
			writer.writerow(data) #write list of values to .csv
			data = []

#================================================================

def createCARTFile(preSet):
	"""
	INPUT: the set of preprocessed words
	OUTPUT: .CSV file for the set readable by CART
	"""	
	with open('Preprocessed_CART.csv', 'wb') as f:
		writer = csv.writer(f)
		columns = []
		data = []
		columns.append('author')
		for word in preSet:
			columns.append(word)	#add words as column headers	
			
		writer.writerow(columns)
		for paper in Papers.allPapers:
			data.append(paper.author) #author initial as first index
			for word in preSet:
				data.append(paper.preDict[word]) #add relative frequency to list

			writer.writerow(data) #write list to .csv
			data = []

#================================================================
if __name__ == '__main__':
	main()
# ===============================================================