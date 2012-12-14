#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.dom.minidom import parseString
import sys, re
import codecs
from spellCorrector import correct

class Normalizer():

	def __init__(self, input, dict, output, corrections):
		self.input = codecs.open(input,'r','utf-8')
		self.output = codecs.open(output,'w','utf-8')
		self.dict = codecs.open(dict,'r','utf-8').read().splitlines()
		self.corrections = codecs.open(corrections,'w','utf-8')

	def is_in_dict(self, word, dict):
		length = len(dict)
		if length == 0:
			return False

		pos = length/2
		if dict[pos] == word:
			return True
		elif dict[pos] < word:
			return self.is_in_dict(word, dict[pos+1:])
		else:
			return self.is_in_dict(word, dict[:pos])

	def start(self):
		content = self.input.read()
		self.dom = parseString(content.encode('utf-8'))
		
		question_answer = self.dom.getElementsByTagName("question") + self.dom.getElementsByTagName("answer")
		for qa in question_answer:
			if qa.childNodes == []:
				continue
			child = qa.childNodes[0]

			tokens = child.nodeValue.split('<br />')
			for token in tokens:
				if not self.is_in_dict(token, self.dict):
					norm = correct(token)
					if norm != token:
						self.corrections.write(token+'\t'+norm+'\n')
						child.nodeValue = child.nodeValue.replace(token, norm)

		self.dom.writexml(self.output)

def parse_options():
	parser = argparse.ArgumentParser()

	parser.add_argument('input', metavar='input', type=str)
	
	parser.add_argument('-d', '--dict', metavar='input', type=str)

	parser.add_argument('-o', '--output', metavar='output', type=str)
	
	parser.add_argument('-c', '--corrections', metavar='corrections', type=str)
	
	return parser.parse_args()

def main():
	args = parse_options()
	t = Normalizer(args.input, args.dict, args.output, args.corrections)
	t.start()

if __name__ == "__main__":
    main()
