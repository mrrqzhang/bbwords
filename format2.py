
import sys
from operator  import itemgetter
from collections import defaultdict
ner=[]
html=''
title=[]
date=''
time=''

nerfile=open(sys.argv[1],'r')
sourcefile=open(sys.argv[2],'r')
termfile=open(sys.argv[3],'w')
contextfile=open(sys.argv[4],'w')

TwoFileFormat=False
urldict=dict()
for line in nerfile:
    fields=line.strip('\r\t\n').split('\t')
    if len(fields)>=3:
        urldict[fields[1]]=fields[2:]   #format: URLID:  URLIDUi0v4SxZppYvnt50n21CwqnoegbUKZUt   CNBC    Business News


entrylist=[]
nerdict=set()
urlid=''

for line in sourcefile:
    line=line.strip('\r\t\n')
    if line[0:5]=='URLID':
	if urlid!='' and urlid in urldict:
                for item in urldict[urlid]: 
		    nerdict.add(item)
                    entrylist.append([item,html,' '.join(title),date,time]) 
#		sys.stdout.write('%s\t%s\t%s\n' % (id,html,' '.join(title)))
        urlid,html=line.split('\t')
        urlid=urlid.strip(':')
	ner=[]
        title=[]
        date=''
        time=''
    elif line[0:4]=='DATE':
        date = 0 if len(line.split('\t'))<2 else line.split('\t')[1]
    elif line[0:4]=='TIME':
        time = 0 if len(line.split('\t'))<2 else line.split('\t')[1]
    elif line[0:5]=='TITLE':
        title.append('' if len(line.split('\t'))<2 else line.split('\t')[1])
	
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
    nerdict2[item]=id
    id+=1

nerlist2 = sorted(entrylist, key=itemgetter(0))
id=1
for item in nerlist2:
    if TwoFileFormat:
    	contextfile.write('%d\t%d\t%s\t%s\t%s %s\n' % (id,nerdict2[item[0]],item[2],item[1],item[3],item[4]))
    else:
        contextfile.write('%s\t%s\t%s\t%s %s\n' % (item[0],item[2],item[1],item[3],item[4]))
    id += 1


termfile.close()
contextfile.close()
