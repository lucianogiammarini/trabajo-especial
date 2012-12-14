#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constants import alphabet
import codecs

class Matrix():
	def __init(self):
		pass
	
	def load(self, filename):
		f = codecs.open(filename,'r','utf-8')
		lines = f.read().splitlines()
		lines = map(lambda x: x.split(u'\t'), lines)
		self.m = map(lambda x: map(int,x), lines)
		f.close()

	def save(self, filename):
		f = codecs.open(filename,'w','utf-8')
		for line in self.m:
			for number in line:
				f.write(str(number)+'\t')
			f.write('\n')
		f.close()

	def get(self, x, y):
		if x == u'@':
			return self.m[len(alphabet), alphabet.find(y)]
		return self.m[alphabet.find(x), alphabet.find(y)]

	def set(self, x, y, n):
		if x == u'@':
			 self.m[len(alphabet), alphabet.find(y)] = n
			 return
		self.m[alphabet.find(x), alphabet.find(y)] = n

def main():
	pass

if __name__ == "__main__":
    main()
