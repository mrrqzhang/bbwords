
import sys

ner=[]
html=''
title=[]

for line in sys.stdin:
    line=line.strip('\r\t\n')
#    print line[0:4]
    if line[0:4]=='http':
	if len(ner)!=0:
            for item in ner: sys.stdout.write('%s\t%s\t%s\n' % (item,html,' '.join(title)))
        html=line
	ner=[]
        title=[]
    elif line[0:3]=='ner':
        ner.append(line.split('\t')[1])
    else:
	title.append(line)
	
if len(ner)!=0:
   for item in ner: sys.stdout.write('%s\t%s\t%s\n' % (item,html,' '.join(title)))

