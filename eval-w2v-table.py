import marisa_trie
import sys,math,string
import json
from mypythonlib import tokenize_punct,doc_tfidf,cosine_score_normalized,cosine



wordvector = json.load(open(sys.argv[1]))
for line in sys.stdin:
    w1,w2 = line.strip('\r\t\n').split('\t')
    if w1 in wordvector and w2 in wordvector:
        relscore=cosine(wordvector[w1],wordvector[w2])
        print (w1,"\t",w2,"\t",relscore)

