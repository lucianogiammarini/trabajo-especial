#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.dom.minidom import parseString
import sys, re
import codecs
from spellCorrector import SpellCorrector

class Normalizer():

	def __init__(self, input, dict, output, corrections):
		self.input = codecs.open(input,'r','utf-8')
		self.output = codecs.open(output,'w','utf-8')
		self.dict = codecs.open(dict,'r','utf-8').read().splitlines()
		self.corrections = codecs.open(corrections,'w','utf-8')
		self.sc = SpellCorrector(dict, '../tokens.count')

	def contains(self, dict, word):
		if word=='para':
			import pdb
			pdb.set_trace()

		length = len(dict)
		if length == 0:
			return False

		pos = length/2
		if dict[pos] == word:
			return True
		elif dict[pos] < word:
			return self.contains(dict[pos+1:], word)
		else:
			return self.contains(dict[:pos], word)

	def start(self):
		content = self.input.read()
		self.dom = parseString(content.encode('utf-8'))
		
		question_answer = self.dom.getElementsByTagName("question") + self.dom.getElementsByTagName("answer")
		trs,tot=0,len(question_answer)
		for qa in question_answer:
			if qa.childNodes == []:
				continue
			child = qa.childNodes[0]
			sys.stdout.write('\r')
			sys.stdout.write("%d/%d" %(trs,tot))
			sys.stdout.flush()
			trs+=1

			tokens = child.nodeValue.split('<br />')
			for token in tokens:
				if len(token) < 2 or not token.isalpha():
					continue
				#if not self.contains(self.dict, token):
				if not token in self.dict:
					norm = self.sc.correct(token)
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
