import marisa_trie
import sys
from mypythonlib import tokenize_punct


trie = marisa_trie.Trie()
with open('/tmp/ruiqiang/bbword/wiki_trie.marisa', 'r') as f:
	trie.read(f)


for line in sys.stdin:
    sent = tokenize_punct(line.strip('\r\t\n'))
    vsent = sent.split()
    entity=[]
    for sp in range(len(vsent)):
        sent2 = ' '.join(vsent[sp:])
        prefix = trie.prefixes(sent2.decode('utf-8'))
#        print prefix
        if len(prefix)==0: continue
        ws = prefix[-1].split()
        if ws[-1]==vsent[sp+len(ws)-1]:
           entity.append([' '.join(ws),sp,sp+len(ws)-1])
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
   

