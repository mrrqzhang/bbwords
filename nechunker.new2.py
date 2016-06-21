import marisa_trie
import sys,math
import json
from mypythonlib import tokenize_punct,doc_tfidf,cosine_with_weights


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

wordvector = json.load(open('/tmp/ruiqiang/wikidump/wiki-test.tfidf.json'))
dfvector = json.load(open('/tmp/ruiqiang/wikidump/wiki-test-df.json'))


for line in sys.stdin:
    print (line)
    fields = line.strip('\r\t\n').split('\t')
    sent = fields[1]
    url = fields[2]
    normaledsent = tokenize_punct(sent.lower())
    lntfidf = doc_tfidf(normaledsent,dfvector)

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
        if vlongest[-1]==vsent[sp+len(vlongest)-1] and (prefix[-1].lower() not in stopwordtrie) and prefix[-1].isdigit()==False and (len(vlongest)>=2 or (sp>0 and vsent[sp-1]!='.')) :
           entity.append([' '.join(vlongest),sp,sp+len(vlongest)-1])
    if len(entity)==0: continue
    print (entity)
#    print (lntfidf, wordvector[cne])

    evals=[]
    longne,lstart,lend='None',-1,-1
    for i in range(0,len(entity)):
        if entity[i][2]<=lend or entity[i][2]-entity[i][1]< lend-lstart: continue # skip inclusive: BC case in ABC or use lognest match  
        if entity[i][1]>lend:  # start new entity after the first
            longne,lstart,lend = entity[i]
            if longne != 'None' and longne in wordvector:
                for origword,fvec in wordvector[longne]:
#                    relscore = cosine_with_weights(fvec,lntfidf)
                    relscore=-1.0
                    evals.append((longne,origword,relscore))
            longne,lstart,lend = entity[i]
#    sys.stdout.write('%s\t%d\t%d\n' % (cne,cstart,cend))    
    for item in evals:
        sys.stdout.write('ner\t%s\t%s\t%f\n' % (item[0],item[1],item[2]))

