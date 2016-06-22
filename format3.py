
import sys
from operator  import itemgetter
from collections import defaultdict
ner=[]
html=''
title=[]
date=''
time=''


TwoFileFormat=False

entrylist=[]
nerdict=set()
urlid=''

for line in sourcefile:
    line=line.strip('\r\t\n')
    if line[0:5]=='URLID':
	if urlid!='' and text!=['']:
            sys.stdout.write('%s\t%s\t%s\n' % (id,html,' '.join(text)))
        urlid,html=line.split('\t')
        urlid=urlid.strip(':')
	ner=[]
        title=[]
        date=''
        time=''
        text=''
    elif line[0:4]=='DATE':
        date = 0 if len(line.split('\t'))<2 else line.split('\t')[1]
    elif line[0:4]=='TIME':
        time = 0 if len(line.split('\t'))<2 else line.split('\t')[1]
    elif line[0:5]=='TITLE':
        title.append('' if len(line.split('\t'))<2 else line.split('\t')[1])
    elif line[0:5]=='TEXT':
        text.append('' if len(line.split('\t'))<2 else line.split('\t')[1])
