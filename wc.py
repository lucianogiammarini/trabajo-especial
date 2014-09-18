#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs

def contains(dictionary, word):
	length = len(dictionary)
	if length == 0:
		return False

	pos = length/2
	if dictionary[pos] == word:
		return True
	elif dictionary[pos] < word:
		return contains(dictionary[pos+1:], word)
	else:
		return contains(dictionary[:pos], word)

class WC():
	""" Determina cuántas palabras del archivo 'tokens' pertenecen al diccionario 'dic' """
	def __init__(self, tokens, dic):
		self.tokens = codecs.open(tokens,'r','utf-8')
		self.dict = codecs.open(dic,'r','utf-8')

	def count(self):
		tokens = self.tokens.read().splitlines()
		dict_words = self.dict.read().splitlines()

		result = 0
		for token in tokens:
			#if token in dict_words:
			if contains(dict_words, token):
				result += 1
		
		print result, ' of ', len(tokens), ' tokens are words.'

def parse_options():
	parser = argparse.ArgumentParser()

	parser.add_argument('tokens', metavar='tokens', type=str)

	parser.add_argument('dict', metavar='dict', type=str)

	return parser.parse_args()

def main():
	args = parse_options()

	wc = WC(args.tokens, args.dict)
	wc.count()

if __name__ == "__main__":
	main()

