#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Spelling Corrector.

Copyright 2007 Peter Norvig. 
Open source code under MIT license: http://www.opensource.org/licenses/mit-license.php
"""

import re, collections
import operator
from corpus import Corpus
from constants import alphabet

def train(features):
	model = collections.defaultdict(lambda: 1)
	for f in features:
		model[f] += 1
	return model

NWORDS = train(file('big.txt').read().splitlines())

def edits1(word):
	s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
	deletes	= [a + b[1:] for a, b in s if b]
	transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
	replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
	inserts	= [a + c + b for a, b in s for c in alphabet]
	return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def rank(candidates, word):
	if len(candidates) == 1:
		return [(candidates.pop(),)]

	c = Corpus("../tokens.count")
	ranking = []

	n = len(word)
	for candidate in candidates:
		ranking.append((candidate,c.probability(candidate)))
		continue

		m = len(candidate)
		i = 0
		while i<min(n,m) and candidate[i]==word[i]:
			i+=1

		print 'candidate ' + candidate + ' '*int(len(candidate)<len(word)+1),
		if n<m: # DELETION
			if i>0:
				print 'del  : ' + candidate[i-1:i+1] + ' typed as ' + candidate[i-1]
			else:
				print 'del  : @' + candidate[i] + ' typed as @'
		elif n>m: # INSERTION
			if i>0:
				print 'ins  : ' + candidate[i-1] + ' typed as ' + word[i-1:i+1]
			else:
				print 'ins  : @ typed as @' + word[i]
		elif n==m:
			if candidate[i+1]==word[i+1]: # SUBSTITUTION
				print 'subs : ' + candidate[i] + ' typed as ' + word[i]
			else: # TRANSPOSITION
				print 'trans: ' + candidate[i:i+2] + ' typed as ' + word[i:i+2]
	
	return sorted(ranking, key=operator.itemgetter(1), reverse=True)

def correct(word):
	if len(known([word])) != 0:
		return word

	candidates = known([word]).union(known(edits1(word)))
	if len(candidates) == 0:
		return word
	return rank(candidates, word)[0][0]

if __name__ == '__main__':
	import sys
	print correct(sys.argv[1])
