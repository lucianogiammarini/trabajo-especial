#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, codecs
import urllib2
import argparse
from bs4 import BeautifulSoup

URL = "http://ask.fm/"

XML_ILLEGAL = [('&', '&amp;'),
				('<', '&lt;'),
				('>', '&gt;'),
				('"', '&quot;'),
				("'", '&#39;')]

def to_valid_xml(content):
	for illegal, legal in XML_ILLEGAL:
		content = content.replace(illegal,legal)
	return content

def create_xml(question, answer, author=None, user=None):
	author_arg = ' author="%s"' %author
	user_arg = ' user="%s"' %user

	xml = '<questionBox%s>\n' %user_arg if user else ''
	xml += '\t<question%s>%s</question>\n' %(author_arg if author else '', to_valid_xml(question))
	if answer != '':
		xml += '\t<answer>%s</answer>\n' %to_valid_xml(answer)
	xml += '</questionBox>\n'
	return xml

def questionBox_filter(tag):
	questionBox = tag.has_key('class') and \
				tag['class'][0] == "questionBox" and tag.div != None
	if questionBox:
		bSlot = tag.div.has_key('class') and \
				tag.div['class'][0] == "bSlot"
		return not bSlot
	return False

def get_question(questionBox):
	question = questionBox.find('span', { "dir" : "ltr" })
	if question != None:
		if question.a != None:
			question.a.extract()	# Elimina todos los links
		return question.get_text(strip=True)
	return None

def get_answer(questionBox):
	answer = questionBox.find('div', { "class" : "answer" })
	if answer != None:
		if answer.a != None:
			answer.a.extract()		# Elimina todos los links
		return answer.get_text(" ", strip=True)
	return None

def get_author(questionBox):
	author = questionBox.find('span', { "class" : "author nowrap" })
	if author != None:
		return author.a['href'][1:]
	return None

class Crawler(object):
	def __init__(self, username, count, ignore=[], visited_fo=None, out=sys.stdout):
		self.visit = [username]
		self.count = count
		self.out = codecs.open(out,'w','utf-8')
		self.ignore = ignore
		self.visited_fo = visited_fo
		self.visited = []

	def crawl(self):
		self.out.write('<?xml version="1.0" encoding="utf-8" ?>\n<root>\n')

		while len(self.visit) > 0 and self.count > 0:
			user = self.visit.pop(0)
			self.visited.append(user)
			content = self.read(URL + user)
			soup = BeautifulSoup(content, from_encoding="utf-8")
			responses = int(soup.find(id='profile_answer_counter').string)
			if responses < 0: 
				continue

			questionBoxes = soup.findAll(questionBox_filter)

			for questionBox in questionBoxes:
				self.parse(questionBox, user)
				self.count -= 1

				sys.stdout.write('\r')
				sys.stdout.write("%d" %self.count)
				sys.stdout.flush()

				if self.count == 0:
					break
		
		self.out.write('</root>')
		if self.count > 0:
			print 'Imposible obtener todas las preguntas. Faltaron %s' %self.count

		if self.visited_fo != None:
			self.visited_fo.writelines(["%s\n" % item for item in self.visited])
			#self.visited_fo.writelines(map(,self.visited))

	def parse(self, questionBox, user=None):
		question = get_question(questionBox)
		answer = get_answer(questionBox)
		author = get_author(questionBox)
		if question == None or answer == None:
			sys.stderr.write('Error al parsear questionBox!!!!!!')

		if author != None and not author in self.visit + self.visited + self.ignore:
			self.visit.append(author)

		self.out.write(create_xml(question,answer,author,user))

	def open(self, url):
		try:
			request = urllib2.Request(url)
			handle = urllib2.build_opener()
		except IOError:
			return None
		return (request, handle)

	def read(self, url):
		request, handle = self.open(url)
		if handle:
			try:
				content = unicode(handle.open(request).read(), "utf-8",	errors="replace")
				return content
			except urllib2.HTTPError, error:
				if error.code == 404:
					print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
				else:
					print >> sys.stderr, "ERROR: %s" % error
				return None
			except urllib2.URLError, error:
				print >> sys.stderr, "ERROR: %s" % error
				return None

class IgnoreAction(argparse.Action):
	def __call__(self, parser, namespace, value, option_string=None):
		ignore = []
		try:
			ignore = map(str.rstrip, value)
			value.close()
			if hasattr(namespace, 'username') and namespace.username in ignore:
				print >> sys.stderr, "ERROR: '%s' no puede estar en la lista de ignorados" % self.username
				sys.exit(-1)
		except:
			print >> sys.stderr, "ERROR"

		setattr(namespace, self.dest, ignore)

class UserAcion(argparse.Action):
	def __call__(self, parser, namespace, value, option_string=None):

		if namespace.ignore != None:
			if value in namespace.ignore:
				print >> sys.stderr, "ERROR: El usuario no puede estar en la lista de ignorados"
				sys.exit(-1)
		else:
			setattr(namespace, 'ignore', [])

		setattr(namespace, self.dest, value)

def parse_options():
	"""
	Parse any command-line options given returning both
	the parsed options and arguments.
	"""

	parser = argparse.ArgumentParser()

	parser.add_argument('-c', '--count', metavar='count', type=int, 
				default=25, help='cantidad de preguntas que deben obtenerse')

	parser.add_argument('-o', '--output', metavar='out', type=str, 
				default=sys.stdout, help='archivo donde se guardaran las preguntas')

	parser.add_argument('-i', '--ignore', metavar='ignore', type=argparse.FileType('r'),
				action=IgnoreAction, help='archivo con usuarios a ignorar')

	parser.add_argument('-v', '--visited', metavar='visited', type=argparse.FileType('w'),
				help='archivo donde se guardaran los usuarios recorridos')

	parser.add_argument('user', metavar='username', action=UserAcion,
				help='usuario inicial')

	return parser.parse_args()

def main():
	args = parse_options()
	c = Crawler(args.user, args.count, args.ignore, args.visited, args.output)
	c.crawl()

if __name__ == "__main__":
    main()
