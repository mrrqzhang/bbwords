import marisa_trie
import sys

input=sys.argv[1]
output=sys.argv[2]
wl=[]

for line in open(input,'r'):
     wl.append(line.strip('\r\t\n').decode('utf-8'))

trie = marisa_trie.Trie(wl)
with open(output, 'w') as f:
     trie.write(f)

