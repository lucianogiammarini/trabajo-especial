#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Spelling Corrector.

Copyright 2007 Peter Norvig. 
Open source code under MIT license: http://www.opensource.org/licenses/mit-license.php
"""

import time
import collections

ALPHABET = u'abcdefghijklmnñopqrstuvwxyz'
DICTIONARY = "/usr/share/dict/spanish";

class Norvig:
	def __init__(self, dictionary, fset):
		self.nwords = self.train(file(dictionary).read().splitlines())
		if fset:
			self.set = frozenset
		else:
			self.set = set

	def train(self, features):
		model = collections.defaultdict(lambda: 1)
		for f in features:
			model[f] += 1
		return model

	def edits1(self, word):
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes	= [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
		replaces   = [a + c + b[1:] for a, b in s for c in ALPHABET if b]
		inserts	= [a + c + b for a, b in s for c in ALPHABET]
		return self.set(deletes + transposes + replaces + inserts)

	def known_edits2(self, word):
		return self.set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.nwords)

	def known(self, words): return self.set(w for w in words if w in self.nwords)

	def search(self, word, max_cost):
		if max_cost == 1:
			return self.known(self.edits1(word))
		else:
			return self.known_edits2(word)

if __name__ == '__main__':
	import sys, resource #@UnresolvedImport

	TARGET = sys.argv[1]
	MAX_COST = int(sys.argv[2])

	start = time.time()
	n = Norvig(DICTIONARY, fset = True)
	end = time.time()
	print "Init took %g s" % (end - start)
		
	start = time.time()
	results = n.search(TARGET, MAX_COST)
	end = time.time()

	for result in results: print result

	print "Search took %g s" % (end - start)
	print "Maximum memory usage %g mb" % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
