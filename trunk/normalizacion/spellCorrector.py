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
from matrix import Matrix

class SpellCorrector:
	def __init__(self, dictionary, corpus): #../extended_dict.txt, ../tokens.count
		self.nwords = self.train(file(dictionary).read().splitlines())
		self.corpus = Corpus(corpus)

		self.deletion = Matrix()
		self.deletion.load('del.txt')
		self.add = Matrix()
		self.add.load('add.txt')
		self.sub = Matrix()
		self.sub.load('sub.txt')
		self.rev = Matrix()
		self.rev.load('rev.txt')

	def train(self, features):
		model = collections.defaultdict(lambda: 1)
		for f in features:
			model[f] += 1
		return model

	def edits1(self, word):
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes	= [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
		replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
		inserts	= [a + c + b for a, b in s for c in alphabet]
		return set(deletes + transposes + replaces + inserts)

	def known_edits2(self, word):
		return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.nwords)

	def known(self, words): return set(w for w in words if w in self.nwords)

	def rank(self, candidates, word):
		if len(candidates) == 1:
			#print_('only candidate ',
			return [(candidates.pop(),)]

		ranking = []
		n = len(word)
		for candidate in candidates:
			m = len(candidate)
			i = 0
			while i<min(n,m) and candidate[i]==word[i]:
				i+=1

			#print candidate + '\t',
			if n<m: # DELETION
				if i>0:
					#print 'del: ' + candidate[i-1:i+1] + '\ttyped as ' + candidate[i-1],
					perror = self.deletion.get(candidate[i-1],candidate[i])/self.corpus.ocurrences(candidate[i-1:i+1])
				else:
					#print 'del: @' + candidate[i] + '\ttyped as @',
					perror = self.deletion.get('@',candidate[i])/self.corpus.ocurrences(candidate[i], start=True)
			elif n>m: # ADDITION
				if i>0:
					#print 'add: ' + candidate[i-1] + '\ttyped as ' + word[i-1:i+1],
					perror = self.add.get(candidate[i-1],word[i])/self.corpus.ocurrences(candidate[i-1])
				else:
					#print 'add: @\ttyped as @' + word[i],
					perror = self.add.get('@',word[i])/self.corpus.ocurrences(word[i], start=True)
			elif n==m:
				if i+1<n and candidate[i+1]!=word[i+1]:# TRANSPOSITION
					#print 'rev: ' + candidate[i:i+2] + '\ttyped as ' + word[i:i+2],
					perror = self.rev.get(candidate[i],candidate[i+1])/self.corpus.ocurrences(candidate[i:i+2])
				else:  # SUBSTITUTION
					#print 'sub: ' + candidate[i] + '\ttyped as ' + word[i],
					perror = self.sub.get(word[i],candidate[i])/self.corpus.ocurrences(candidate[i])
		
			model = self.corpus.probability(candidate)
			ranking.append((candidate,perror*model))
			#print '\n\tperror: ', perror, '\tprob(%s): '%candidate, model, '\n\ttotal: ', perror*model
		
		return sorted(ranking, key=operator.itemgetter(1), reverse=True)

	def correct(self, word):
		candidates = self.known(self.edits1(word))
		if len(candidates) == 0:
			return word # no se encontro ninguna correccion
		return self.rank(candidates, word)[0][0]

if __name__ == '__main__':
	import sys
	sc = SpellCorrector('../extended_dict.txt', '../tokens.count')
	word = sys.argv[1]
	if len(sc.known([word])) != 0: # Si la palabra es conocida no hay que corregirla
		print 'is in dict',
	else:
		print sc.correct(word)
