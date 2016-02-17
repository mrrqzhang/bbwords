
import sys
import operator

entitylist=dict()
for line in sys.stdin:
    entity=''
    words = line.strip('\r\n\t').split()
    pre_p='O'
    for token in words:
      try:
        w,p = token.split('/')
      #  print w,p
        if p=='O': 
             entity=entity+'\n'
             pre_p=p
        elif p==pre_p:
             entity = entity+' '+w
             pre_p=p
        else: 
	     entity = entity+'\n'+w
             pre_p=p
      except: pass
    for token in entity.split('\n'):
        if entitylist.has_key(token): entitylist[token]+=1
        else: entitylist.setdefault(token,1)
if entitylist.has_key(''):
    del entitylist['']

for key in sorted(entitylist.items(),key=operator.itemgetter(1),reverse=True):
#     print key
    sys.stdout.write('ner\t%s\t%d\n' % (key[0],key[1]))
