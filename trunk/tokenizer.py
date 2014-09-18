#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.dom.minidom import parseString
import codecs

EMOT = [':S',':D',':O',':P',':3',':V','<3','=D','=P','8)','8|','B)','B|',':-D',':-O',
		':-P','>:O','3:)','8-)','8-|','B-|','O:)']
EXP = '([^ABCDEFGHIJKLMNOPQRSTUVWXYZÁÉÍÓÚÑabcdefghijklmnopqrstuvwxyzáéíóúñ]*)'

def flattener(lst):
	return [item for sublist in lst for item in sublist if item != '']

def enum(**enums):
	return type('Enum', (), enums)

Type = enum(SYMBOL=0, DIGIT=1, ALPHA=2, SPACE=3)

class Tokenizer():

	def __init__(self, input_filename, output_filename, lowercase, tokens=None):
		self.input = codecs.open(input_filename,'r','utf-8')
		self.output = codecs.open(output_filename,'w','utf-8')
		if tokens:
			self.tokens = codecs.open(tokens,'w','utf-8')
		else:
			self.tokens = None
		self.lowercase = lowercase

	def start(self):
		content = self.input.read()
		if self.lowercase:
			content = content.lower().replace('questionbox','questionBox')
			#tokens = map(unicode.lower,tokens)

		self.dom = parseString(content.encode('utf-8'))
		question_boxes = self.dom.getElementsByTagName("questionBox")
		
		for box in question_boxes:
			question = box.getElementsByTagName("question")
			if question == [] or question[0].firstChild == None:
				continue
			self.tokenize(question[0])
			
			answer = box.getElementsByTagName("answer")
			if answer == [] or answer[0].firstChild == None:
				continue
			self.tokenize(answer[0])

		self.output.write(self.dom.toxml())

	def type(self, char):
		if char.isalpha():
			return Type.ALPHA
		elif char.isdigit():
			return Type.DIGIT
		elif char.isspace():
			return Type.SPACE
		else:
			return Type.SYMBOL

	def tokenize(self, element):
		text = element.firstChild.nodeValue
		length = len(text)
		if length == 0:
			return

		prevType = self.type(text[0])
		tokens = [text[0]]
		pos = 1
		while pos < length:
			t_type = self.type(text[pos])

			# si es emoticon de tres caracteres o es digit[.,]digit los dejo juntos
			if pos+2 <= length and (text[pos-1:pos+2].upper() in EMOT or 
					(prevType == self.type(text[pos+1]) == Type.DIGIT and 
					text[pos] in ['.',','])):
				tokens[-1] += text[pos:pos+2]
				prevType = self.type(text[pos+1])
				pos+=2
				continue
			# si es emoticon de dos caracteres
			if text[pos-1:pos+1].upper() in EMOT:
				tokens[-1] += text[pos]
				prevType = t_type
				pos+=1
				continue

			if t_type != prevType and t_type != Type.SPACE:
				# Si es distinto al anterior es un nuevo token
				tokens.append(text[pos])
			elif t_type != Type.SPACE: 
				# Si es igual al anterior pertenece al mismo token
				# Pero no se agrega si es un espacio
				tokens[-1] += text[pos]

			prevType = t_type
			pos+=1

		element.removeChild(element.childNodes[0])
		element.appendChild(self.dom.createTextNode('</br>'.join(tokens)))
		if self.tokens:
			self.tokens.write('\n'.join(tokens)+'\n')

def parse_options():
	parser = argparse.ArgumentParser()

	parser.add_argument('input', metavar='input', type=str)

	parser.add_argument('-o', '--output', metavar='output', type=str)
	
	parser.add_argument('-l', '--lowercase', action='store_true', default=False)
	
	parser.add_argument('-t', '--tokens', metavar='tokens', type=str, 
				help='File to save only tokens')

	return parser.parse_args()

def main():
	args = parse_options()
	t = Tokenizer(args.input, args.output, args.lowercase, args.tokens)
	t.start()

if __name__ == "__main__":
	main()
