#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator, codecs

def contains(dict, word):
	length = len(dict)
	if length == 0:
		return False

	pos = length/2
	if dict[pos] == word:
		return True
	elif dict[pos] < word:
		return contains(dict[pos+1:], word)
	else:
		return contains(dict[:pos], word)

class Corpus:
	def __init__(self, filename):
		self.cache = {}
		self.words = []
		self.total = 0.0
		lines = codecs.open(filename,'r','utf-8').read().splitlines()
		for line in (lines):
			count,word = tuple(line.split())
			self.words.append((word,int(count)))
			self.total += int(count)

		self.words = sorted(self.words, key=operator.itemgetter(0))
		self.length_lex = len(self.words)
		#lista de tupla (palabra, nro de ocurrencias) ordenada por palabra

	def ocurrences(self, subword):
	# Cuenta la cantidad de ocurrencias de subword en todas las palabras
		if subword in self.cache:
			print 'cache'
			return self.cache[subword]

		c = 0
		for word,count in self.words:
			c += word.count(subword)

		self.cache[subword] = c
		return c

	def probability(self, word):
		# add one smoothing
		return (self.count(word, self.words)+1.0)/(self.total+self.length_lex)

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

