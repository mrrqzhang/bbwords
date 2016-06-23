import marisa_trie
import sys,math
import json
from mypythonlib import tokenize_punct,doc_tfidf,cosine_with_weights,cosine


trie = marisa_trie.Trie()
with open('/tmp/ruiqiang/git_mrrqzhang/bbwords/wiki_trie.norm.marisa', 'r') as f:
	trie.read(f)

stopwordtrie = marisa_trie.Trie()
with open('/tmp/ruiqiang/git_mrrqzhang/bbwords/stopwords.marisa', 'r') as f:
        stopwordtrie.read(f)

def any_capitalized(word):
    for item in word:
        if item == item.capitalize(): return True
    return False

def all_capitalized(word):
    for item in word:
        if item != item.capitalize(): return False
    return True

wordvector = json.load(open('/tmp/ruiqiang/wikidump/wikiname.json'))

firstkey=list(wordvector.keys())[0]

for line in sys.stdin:
    fields = line.strip('\r\t\n').split('\t')
    sent = fields[2]
    url = fields[1]
    normaledsent = tokenize_punct(sent.lower())

    vsent = normaledsent.split()
    entity=[]
    for sp in range(len(vsent)):
        wordtoend = ' '.join(vsent[sp:])
        prefix = trie.prefixes(wordtoend)
#        print prefix
        if len(prefix)==0: continue
        # longest prefix
        vlongest = prefix[-1].split() 
        # two words or non-punc single word
        if vlongest[-1]==vsent[sp+len(vlongest)-1] and (prefix[-1].lower() not in stopwordtrie) and prefix[-1].isdigit()==False : # and (len(vlongest)>=2 or (sp>0 and vsent[sp-1]!='.')) :
           entity.append([' '.join(vlongest),sp,sp+len(vlongest)-1])
    if len(entity)==0: continue

    evals=[]
    longne,lstart,lend=entity[0]
    entity.append((firstkey,len(vsent),2*len(vsent)))  # to output last entity
    for i in range(1,len(entity)):
        if entity[i][0] not in wordvector: continue
        if entity[i][2]<=lend or ( entity[i][1]<lend and entity[i][2]-entity[i][1]< lend-lstart): continue # skip inclusive: BC case in ABC or use lognest match  
        if entity[i][1]>lend:  # start new entity after the first
            if longne in wordvector:
                evals.append(longne)
            longne,lstart,lend = entity[i]
#    sys.stdout.write('%s\t%d\t%d\n' % (cne,cstart,cend))    
    for item in evals:
        sys.stdout.write('%s\n' % item)
