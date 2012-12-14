#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator, codecs

class Corpus:
	def __init__(self, filename):
		self.words = []
		self.total = 0.0
		lines = codecs.open(filename,'r','utf-8').read().splitlines()
		for line in (lines):
			count,word = tuple(line.split())
			self.words.append((word,int(count)))
			self.total += int(count)

		self.words = sorted(self.words, key=operator.itemgetter(0))

	# Cuenta la cantidad de ocurrencias de subword en todas las palabras
	def ocurrences(self, subword):
		c = 0
		for word,count in self.words:
			c += word.count(subword)
		return c

	def probability(self, word):
		return self.count(word, self.words)/self.total

	def count(self, word, words):
		length = len(words)
		if length == 0:
			return 0

		pos = length/2
		if words[pos][0] == word:
			return words[pos][1]
		elif words[pos][0] < word:
			return self.count(word, words[pos+1:])
		else:
			return self.count(word, words[:pos])

if __name__ == '__main__':
	import sys
	c = Corpus("../tokens.count")
	print c.probability(sys.argv[1])
	print c.ocurrences(sys.argv[2])
