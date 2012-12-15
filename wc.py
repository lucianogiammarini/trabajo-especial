#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys, re
import codecs

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

class WC():
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

