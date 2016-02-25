
import sys
from operator  import itemgetter
ner=[]
html=''
title=[]
date=''
time=''

termfile=open(sys.argv[1],'w')
contextfile=open(sys.argv[2],'w')

entrylist=[]
nerdict=set()

for line in sys.stdin:
    line=line.strip('\r\t\n')
    if line[0:4]=='URL:':
	if len(ner)!=0:
            for item in ner: 
		nerdict.add(item)
                entrylist.append([item,html,' '.join(title),date,time]) 
#		sys.stdout.write('%s\t%s\t%s\n' % (id,html,' '.join(title)))
        html=line.split('\t')[1]
	ner=[]
        title=[]
        date=''
        time=''
    elif line[0:3]=='NER':
        ner.append(line.split('\t')[1])
    elif line[0:4]=='DATE':
        date = line.split('\t')[1]
    elif line[0:4]=='TIME':
        time = line.split('\t')[1]
    elif line[0:5]=='TITLE':
        title.append(line.split('\t')[1])
	
if len(ner)!=0:
   for item in ner:
        nerdict.add(item)
	entrylist.append([item,html,' '.join(title),date,time])
#       sys.stdout.write('%s\t%s\t%s\n' % (id,html,' '.join(title)))

nerlist = sorted(nerdict)
nerdict2 = dict()
id=1
for item in nerlist:
    termfile.write('%d\t%s\n' %(id,item))
    nerdict2.setdefault(item, id)
    id+=1

nerlist2 = sorted(entrylist, key=itemgetter(0))
id=1
for item in nerlist2:
    contextfile.write('%d\t%d\t%s\t%s\t%s\t%s\n' % (id,nerdict2[item[0]],item[2],item[1],item[3],item[4]))
    id += 1


termfile.close()
contextfile.close()
