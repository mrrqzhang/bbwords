import marisa_trie
import sys,math,string
import json
from mypythonlib import tokenize_punct,doc_tfidf,cosine_score_normalized,cosine


trie = marisa_trie.Trie()
with open('/tmp/ruiqiang/git_mrrqzhang/bbwords/wiki_trie.norm.marisa', 'r') as f:
	trie.read(f)

stopwordtrie = marisa_trie.Trie()
with open('/tmp/ruiqiang/git_mrrqzhang/bbwords/stopwords.marisa', 'r') as f:
        stopwordtrie.read(f)

def any_title_capitalized(word):
    for item in word:
        if item == item.title() or item==item.capitalize(): return True
    return False

def all_capitalized(word):
    for item in word:
        if item != item.capitalize(): return False
    return True

wordvector = json.load(open('/tmp/ruiqiang/wikidump/wiki-test.tfidf.json'))
dfvector = json.load(open('/tmp/ruiqiang/wikidump/wiki-test-article.tfidf.json'))

firstkey=list(wordvector.keys())[0]

for line in sys.stdin:
    print (line)
    fields = line.strip('\r\t\n').split('\t')
    sent = fields[2]
    url = fields[1]
    if url not in dfvector: continue
    lntfidf = dfvector[url]
    normaledsent = tokenize_punct(sent.lower())
   
    uppersent = tokenize_punct(sent)
    vuppersent = uppersent.split()
    vsent = normaledsent.split()
    entity=[]
    for sp in range(len(vsent)):
        wordtoend = ' '.join(vsent[sp:])
        prefix = trie.prefixes(wordtoend)
#        print prefix
        if len(prefix)==0: continue
        # longest prefix
        vlongest = prefix[-1].split() 
        # two words or non-punc single word . NE can't be after punctunation (first word capitalized)
        if vlongest[-1]==vsent[sp+len(vlongest)-1] and (prefix[-1].lower() not in stopwordtrie) and prefix[-1].isdigit()==False: #  and (len(vlongest)>=2 or (sp>0 and vsent[sp-1]!='.')) :
            if not any_title_capitalized(vuppersent[sp:sp+len(vlongest)]): continue #must one capitalized
            # dont count first word capitalized @sent start
#            print ('sp=',sp, vsent[sp-1:sp], vlongest, (vsent[sp-1] in string.punctuation))
            if ( ((sp==0)  or (sp>0 and vsent[sp-1] in string.punctuation) ) and any_title_capitalized(vuppersent[sp]) and not any_title_capitalized(vuppersent[sp+1:sp+len(vlongest)]) ): continue  
            entity.append([' '.join(vlongest),sp,sp+len(vlongest)-1])
    if len(entity)==0: continue
#    print (entity)

    evals=[]
    longne,lstart,lend=entity[0]
    entity.append((firstkey,len(vsent),2*len(vsent)))  # to output last entity
    for i in range(1,len(entity)):
#        print ('entity=',entity[i])
#        print ('last=',longne,lstart,lend)
        if entity[i][0] not in wordvector: continue
#        print ('entity in wordvector')
        if entity[i][2]<=lend or ( entity[i][1]<lend and  entity[i][2]-entity[i][1]< lend-lstart) : continue # skip inclusive: BC case in ABC or use lognest match  
        if entity[i][1]>lend:  # start new entity after the first
            if longne in wordvector:
                for origword,fvec in wordvector[longne]:
                    relscore = cosine(fvec,lntfidf) #cosine_score_normalized(fvec,lntfidf)
#                    relscore=-1.0
                    evals.append((longne,origword,relscore))
            longne,lstart,lend = entity[i]
#    sys.stdout.write('%s\t%d\t%d\n' % (cne,cstart,cend))    
    for item in sorted(evals, key=lambda x:(x[0],x[2]), reverse=True):
        sys.stdout.write('ner\t%s\t%s\t%f\n' % (item[0],item[1],item[2]))

