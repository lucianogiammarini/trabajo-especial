#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from xml.dom.minidom import parseString
import sys, re
import codecs

USERS = 407.0

class Word(object):
	def __init__(self, letter=None, parent=None):
		self._parent = parent
		self._letter = letter
		self._children = {}
		self._count = 0
		self._usersCount = 0
		self._lastUser = None

	def add(self, word, user):
		if len(word) == 0:
			self._count += 1
			if self._lastUser != user:
				self._usersCount += 1
				self._lastUser = user
		else:
			letter = word[0]
			if not self._children.has_key(letter):
				self._children[letter] = Word(letter, self)
			self._children[letter].add(word[1:],user)

	def count(self, out):
		if self._count > 0:
			self._print(out)
			out.write('\t%s\t%s\t%s\n' %(self._count, self._usersCount, self._count*self._usersCount/USERS))
		for child in self._children.values():
			child.count(out)

	def _print(self, out):
		if self._parent != None:
			self._parent._print(out)
			if self._letter != None:
				out.write(self._letter)

	def __str__(self):
		return  str(self._count) +' '+ str(self._usersCount) +' '+ str(self._lastUser)

class Counter():
	def __init__(self, input, output):
		self.input = codecs.open(input,'r','utf-8')
		self.output = codecs.open(output,'w','utf-8')

		self.parent = Word()

	def start(self):
		content = self.input.read()

		self.dom = parseString(content.encode('utf-8'))
		question_boxes = self.dom.getElementsByTagName("questionBox")
		
		for box in question_boxes:
			user = box.getAttribute('user')
			assert(user != '')

			question = box.getElementsByTagName("question")
			if question == [] or question[0].firstChild == None:
				continue
			words = question[0].firstChild.wholeText.split('</br>')
			for word in words:
				self.parent.add(word, user)
			
			answer = box.getElementsByTagName("answer")
			if answer == [] or answer[0].firstChild == None:
				continue
			words = answer[0].firstChild.wholeText.split('</br>')
			for word in words:
				self.parent.add(word, user)

		self.parent.count(self.output)

def parse_options():
	parser = argparse.ArgumentParser()

	parser.add_argument('input', metavar='input', type=str)

	parser.add_argument('-o', '--output', metavar='output', type=str)

	return parser.parse_args()

def main():
	args = parse_options()

	print "Cantidad de usuarios: ", int(USERS)
	# wc -l visited.txt (obtenido de ejecutar crawler -v)

	c = Counter(args.input, args.output)
	sys.setrecursionlimit(50000)
	c.start()

if __name__ == "__main__":
    main()

