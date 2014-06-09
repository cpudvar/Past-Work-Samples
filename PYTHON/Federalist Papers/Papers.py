from collections import Counter
import sets
import string

class Papers(object):
    totalWords = 0 #count of total words across corpus
    allPapers = [] #list of all paper objects
    meanFrequency = .05
    
#=====================================================    
    def __init__(self):
	    """CTOR"""
            
	    self.author = None #author (initial)
	    self.number = None #paper number
	    self.path = None   #FED_author_number.txt
	    self.words = 0     #words in given paper
	    self.text = ""     #the paper
	    self.paperSet = set()	#set of unique words in paper
	    self.paperDict = Counter()  #dictionary of words and their counts
	    
	    self.rawDict = Counter()    #refined dictionary of raw words only
	    self.preDict = Counter()    #refined dictionary of preprocessed words only
	    
#=====================================================   