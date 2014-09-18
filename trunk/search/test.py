from levenshteinTrie import LevenshteinTrie
from levenshtein import Levenshtein
from norvig import Norvig

import sys, time
import codecs

DICTIONARY = "/usr/share/dict/spanish";
TARGETS = sys.argv[1]
MAX_COST = int(sys.argv[2])

targets = codecs.open(TARGETS,'r','utf-8').read().splitlines()[:500]
print "dictionary length: %s" %len(open(DICTIONARY).readlines())
print "targets length: %s\n" %len(targets)

#targets = open(TARGETS, "rt").read().split()

#### Norvig with set ####

start = time.time()
n = Norvig(DICTIONARY, fset = False)
end = time.time()
print "NORVIG (with SET)\ninit took: %g s" % (end - start)

start = time.time()
for target in targets:
	n.search( target, 1 )
end = time.time()

print "known_edits1 search took: %g s\n" % (end - start)

start = time.time()
for target in targets:
	n.search( target, 2 )
end = time.time()

print "known_edits2 search took: %g s\n" % (end - start)

#### Norvig with frozenset ####

start = time.time()
n = Norvig(DICTIONARY, fset = True)
end = time.time()
print "NORVIG (with FROZENSET)\ninit took: %g s" % (end - start)

start = time.time()
for target in targets:
	n.search( target, 1 )
end = time.time()

print "known_edits1 search took: %g s\n" % (end - start)

start = time.time()
for target in targets:
	n.search( target, 2 )
end = time.time()

print "known_edits2 search took: %g s\n" % (end - start)

#### LevenshteinClassic ####

start = time.time()
lev = Levenshtein(DICTIONARY)
end = time.time()
print "LEVENSHTEIN\ninit took: %g s" % (end - start)

start = time.time()
for target in targets:
	lev.search( target, MAX_COST )
end = time.time()

print "search took: %g s\n" % (end - start)


#### LevenshteinTrie ####

start = time.time()
trie = LevenshteinTrie(DICTIONARY)
end = time.time()
print "LEVENSHTEIN TRIE\ninit took: %g s" % (end - start)

start = time.time()
for target in targets:
	trie.search( target, MAX_COST )
end = time.time()

print "search took: %g s\n" % (end - start)
