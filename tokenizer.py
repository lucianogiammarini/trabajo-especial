#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.dom.minidom import parseString
import sys, re
import codecs

EXP = '([^ABCDEFGHIJKLMNOPQRSTUVWXYZ¡…Õ”⁄‹—abcdefghijklmnopqrstuvwxyz·ÈÌÛ˙¸Ò]*)'
def flattener(lst):
    return [item for sublist in lst for item in sublist if item != '']

class Tokenizer(object):
	def __init__(self, input, output, lowercase):
		self.input = codecs.open(input,'r','utf-8')
		self.output = codecs.open(output,'w','utf-8')
		self.lowercase = lowercase
		self.tokens = u''

	def start(self):
		content = self.input.read()

		dom = parseString(content.encode('utf-8'))
		question_boxes = dom.getElementsByTagName("questionBox")
		
		for box in question_boxes:
			question = box.getElementsByTagName("question")
			if question == [] or question[0].firstChild == None:
				continue
			self.tokens += self.tokenize(question[0].firstChild.nodeValue)

			answer = box.getElementsByTagName("answer")
			if answer == [] or answer[0].firstChild == None:
				continue
			self.tokens += self.tokenize(answer[0].firstChild.nodeValue)

		if self.lowercase:
			self.tokens = self.tokens.lower()
		self.output.write(self.tokens)

	def tokenize(self, text):
		s = re.split('\s', text)
		x = flattener(map(lambda x: re.split(EXP, x), s))
		return '<s>' + '<br/>'.join(x) + '</s>\n'

def parse_options():
	parser = argparse.ArgumentParser()

	parser.add_argument('input', metavar='input', type=str)

	parser.add_argument('-o', '--output', metavar='output', type=str)
	
	parser.add_argument('-l', '--lowercase', action='store_true', default=False)

	return parser.parse_args()

def main():
	args = parse_options()
	t = Tokenizer(args.input, args.output, args.lowercase)
	t.start()

if __name__ == "__main__":
    main()
