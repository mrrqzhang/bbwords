import marisa_trie
import sys
import mypythonlib

output=sys.argv[1]
wl=[] 

for line in sys.stdin:
    fields = line.strip('\r\t\n').split('\t')
    nword = mypythonlib.normalize_wiki_entity(fields[0])
    if nword and [nword] != wl[-1:]: 
        wl.append(nword.decode('utf-8'))
trie = marisa_trie.Trie(wl)
with open(output, 'w') as f:
     trie.write(f)

