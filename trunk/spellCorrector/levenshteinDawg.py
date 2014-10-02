'''
Created on 19/9/2014

@author: luciano
'''
from dawg import Dawg
import codecs, time

DICTIONARY = "/usr/share/dict/spanish";

class LevenshteinDawg:
	def __init__( self, dictionary ):

		# read dictionary file into a trie
		self.trie = Dawg()
		words = codecs.open(dictionary,'rt','utf-8').read().split()
		words.sort()
		#words = ["ababol","matar"]
		for word in words:
			self.trie.insert( word )
		self.trie.finish()

	# The search function returns a list of all words that are less than the given
	# maximum distance from the target word
	def search( self, word, maxCost ):

		# build first row
		currentRow = range( len(word) + 1 )

		results = []

		node = self.trie.root
		# recursively search each branch of the trie
		for letter in node.edges:
			self.searchRecursive( node.edges[letter], letter, word, 
								[None, currentRow], results, maxCost )

		return results

	# This recursive helper is used by the search function above. It assumes that
	# the previousRow has been filled in already.
	def searchRecursive( self, node, currentWord, word, previousRows, results, maxCost ):
		letter = currentWord[-1]
		columns = len( word ) + 1
		currentRow = [ previousRows[1][0] + 1 ]

		# Build one row for the letter, with a column for each letter in the target
		# word, plus one for the empty string at column 0
		for column in xrange( 1, columns ):

			cost = int( word[column - 1] != letter )
			insertCost = currentRow[column - 1] + 1
			deleteCost = previousRows[1][column] + 1
			replaceCost = previousRows[1][ column - 1 ] + cost

			minimum = min( insertCost, deleteCost, replaceCost )
			
			if previousRows[0] != None and column > 1 and \
				word[column - 1] == currentWord[-2] and word[column - 2] == letter:

				transpositionCost = previousRows[0][column - 2] + cost
				minimum = min( minimum, transpositionCost )

			currentRow.append( minimum )

		# if the last entry in the row indicates the optimal cost is less than the
		# maximum cost, and there is a word in this trie node, then add it.
		if currentRow[-1] <= maxCost and node.final:
			results.append( (currentWord, currentRow[-1] ) )

		# if any entries in the row are less than the maximum cost, then 
		# recursively search each branch of the trie
		if min( currentRow ) <= maxCost:
			for letter in node.edges:
				self.searchRecursive( node.edges[letter], currentWord+letter, 
									word, [previousRows[1], currentRow], 
									results, maxCost )

if __name__ == '__main__':
	import sys, resource #@UnresolvedImport

	TARGET = sys.argv[1]
	MAX_COST = int(sys.argv[2])
	if len(sys.argv) > 3:
		dictionary = sys.argv[3]
	else:
		dictionary = DICTIONARY

	lev = LevenshteinDawg(dictionary)

	start = time.time()
	results = lev.search( TARGET, MAX_COST )
	end = time.time()

	#for result in results: print result
	for result in results:
		print result[0], result[1]

	print "\nSearch took %g s" % (end - start)
	print "Maximum memory usage %g mb" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
