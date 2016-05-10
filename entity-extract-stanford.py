#entity count, entity bigram count
import sys
import operator
from collections import defaultdict

urlid=''
entitycount=defaultdict(int)
bigramcount=defaultdict(int)
data = sys.stdin.read()

prep='O'
entitylist=set()
entity=''
for word in data.split():
  try:
    w,p = word.split('/')
    if w[0:5]=='URLID':
        sys.stdout.write('\t%s' % '\t'.join(entitylist)) 
        sys.stdout.write('\nURLID:\t%s' % w)
        entitylist.clear()
        entity=''
    elif p=='O':
        if entity:
            entitylist.add(entity)
    elif  p==prep: 
        entity+=' '+w
    else:
        entity=w
    prep=p
  except:
      pass
