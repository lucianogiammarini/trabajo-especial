#!/usr/bin/env python
# -*- coding: utf-8 -*-

# By Steve Hanov, 2011. Released to the public domain.
import codecs, time
ALPHABET = u'abcdefghijklmnopqrstuvwxyzáéíñóúü'

DICTIONARY = "/usr/share/dict/spanish"

from dawg import Dawg, DawgNode

class NumberedDawgNode( DawgNode ):

	def __init__( self ):
		#super(NumberedDawgNode, self).__init__()
		DawgNode.__init__(self)
		self.number = None

class NumberedDawg( Dawg ):

	def finish( self ):
		#super(self.__class__, self).finish()
		Dawg.finish(self)
		self.numbering(self.root)
	
	def numbering( self , node ):
		children = node.edges.values()
		if len(children) == 0:
			node.number = int(node.final)
			return node.number
		
		sum = int(node.final)  # @ReservedAssignment
		for child in children:
			sum += self.numbering(child)
		
		node.number = sum
		return node.number
	
	def wordToIndex( self, word ):
		index = 0
		currentState = self.root
		for letter in word:
			keys = currentState.edges.keys()
			keys.sort()
			if letter in keys:
				for c in keys[:keys.index(letter)]: # for c firstLetter to predecessor(letter)
					if c in keys:
						index += currentState.edges[c].number
				currentState = currentState.edges[letter]
				if currentState.final:
					index += 1
			else:
				return -1

		if currentState.final:
			return index
		else:
			return -1

	def indexToWord( self, index ):
		currentState = self.root
		count = index
		word = ''

		while count > 0:
			for c in ALPHABET:
				if c in currentState.edges.keys():
					auxState = currentState.edges[c]
					if auxState.number < count:
						count -= auxState.number
					else:
						word += c
						currentState = auxState
						if currentState.final:
							count -= 1
							break

		return word
		

if __name__ == '__main__':
	import sys, resource #@UnresolvedImport
	QUERY = sys.argv[1:]

	dawg = NumberedDawg()
	WordCount = 0
	words = codecs.open(DICTIONARY,'rt','utf-8').read().split()
	#words = ['uno', 'dos', 'tres']
	words.sort()

	start = time.time()
	for word in words:
		WordCount += 1
		dawg.insert(word)
		#if ( WordCount % 100 ) == 0: print "%dr" % WordCount,
	dawg.finish()

	print "Dawg creation took %g s" % (time.time()-start)
	
	for word in QUERY:
		if not dawg.lookup( word ):
			print "%s not in dictionary." % word
		else:
			print "%s is in the dictionary. index: %s" % (word, dawg.wordToIndex(word))

	print "Maximum memory usage %g mb" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
