import marisa_trie
import sys

wl=[]

for line in open('/tmp/ruiqiang/wikidump/total-entities.canon.txt','r'):
     wl.append(line.strip('\r\t\n').decode('utf-8'))

trie = marisa_trie.Trie(wl)
with open('wiki_trie.marisa', 'w') as f:
     trie.write(f)

