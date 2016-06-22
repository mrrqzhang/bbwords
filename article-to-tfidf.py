import marisa_trie
import sys,math
import json
from mypythonlib import tokenize_punct,doc_tfidf,cosine_with_weights



def any_capitalized(word):
    for item in word:
        if item == item.capitalize(): return True
    return False

def all_capitalized(word):
    for item in word:
        if item != item.capitalize(): return False
    return True

dfvector = json.load(open('/tmp/ruiqiang/wikidump/wiki-test-df.json'))


for line in sys.stdin:
    fields = line.strip('\r\t\n').split('\t')
    sent = fields[2]
    url = fields[1]
    normaledsent = tokenize_punct(sent.lower())
    lntfidf = doc_tfidf(normaledsent,dfvector)

    for item in lntfidf:
        sys.stdout.write('%s\t%s\t%f\t%s\n' % (url,item[0],item[1],sent))

