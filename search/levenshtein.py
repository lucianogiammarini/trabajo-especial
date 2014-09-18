#!/usr/bin/python
#By Steve Hanov, 2011. Released to the public domain
import codecs, time

DICTIONARY = "/usr/share/dict/spanish";

class Levenshtein:
	# for brevity, we omit transposing two characters. Only inserts,
	# removals, and substitutions are considered here.

	def __init__( self, dictionary ):
		self.words = codecs.open(dictionary,'rt','utf-8').read().split()

	def levenshtein( self, word1, word2 ):
		columns = len(word1) + 1
		rows = len(word2) + 1

		# build first row
		currentRow = [0]
		for column in xrange( 1, columns ):
			currentRow.append( currentRow[column - 1] + 1 )

		for row in xrange( 1, rows ):
			previousRow = currentRow
			currentRow = [ previousRow[0] + 1 ]

			for column in xrange( 1, columns ):

				insertCost = currentRow[column - 1] + 1
				deleteCost = previousRow[column] + 1

				if word1[column - 1] != word2[row - 1]:
					replaceCost = previousRow[ column - 1 ] + 1
				else:
					replaceCost = previousRow[ column - 1 ]

				currentRow.append( min( insertCost, deleteCost, replaceCost ) )

		return currentRow[-1]

	def search( self, target, maxCost ):
		results = []
		for word in self.words:
			cost = self.levenshtein( target, word )

			if cost <= maxCost:
				results.append( (word, cost) )

		return results

if __name__ == '__main__':
	import sys

	TARGET = sys.argv[1]
	MAX_COST = int(sys.argv[2])

	# read dictionary file
	words = codecs.open(dictionary,'rt','utf-8').read().split()


	start = time.time()
	results = search( TARGET, MAX_COST )
	end = time.time()

	for result in results: print result

	print "Search took %g s" % (end - start)
