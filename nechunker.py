import marisa_trie
import sys
from mypythonlib import tokenize_punct


trie = marisa_trie.Trie()
with open('/tmp/ruiqiang/bbword/wiki_trie.marisa', 'r') as f:
	trie.read(f)

tokentrie = marisa_trie.Trie()
with open('/tmp/ruiqiang/bbword/qlas_token.marisa', 'r') as f:
        tokentrie.read(f)


def any_capitalized(word):
    for item in word:
        if item == item.capitalize(): return True
    return False

for line in sys.stdin:
    sent = tokenize_punct(line.strip('\r\t\n'))
    capivsent = sent.split()
    vsent = sent.lower().split()
    entity=[]
    for sp in range(len(vsent)):
        sent2 = ' '.join(vsent[sp:])
        prefix = trie.prefixes(sent2.decode('utf-8'))
#        print prefix
        if len(prefix)==0: continue
        ws = prefix[-1].split()
        if ws[-1]==vsent[sp+len(ws)-1] and ((' '.join(ws)) not in tokentrie) and any_capitalized(capivsent[sp:sp+len(ws)]) and (' '.join(ws)).isdigit()==False:
           entity.append([' '.join(capivsent[sp:sp+len(ws)]),sp,sp+len(ws)-1])
    if len(entity)==0: continue
    cne,cstart,cend = entity[0]
    for i in range(1,len(entity)):
        if entity[i][2]<=cend: continue  
        if entity[i][1]>cend: 
	    sys.stdout.write('ner\t%s\n' % (cne))
	    cne,cstart,cend = entity[i]
        else: 
           if entity[i][2]-entity[i][1]< cend-cstart:
		continue
           else:
	        cne,cstart,cend = entity[i] 
#    sys.stdout.write('%s\t%d\t%d\n' % (cne,cstart,cend))    
    sys.stdout.write('ner\t%s\n' % (cne))
   

