#!/usr/bin/python

import sys, getopt
import subprocess

execdir='/home/ruiqiang/Filers/ss05_ruiqiang/bombwords/git_mrrqzhang/bbwords'

def main(argv):
    crawldomain = ''
    outputfile = ''
    outputdir='./'
    start=int(0)
    end=int(0)
    excludeurls=''
    excludeurlset=[]

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hs:e:c:d:u:",["outputdir=","crawldomain=","start=","end=","exclude-urls="])
    except getopt.GetoptError:
       sys.exit(2)
    print  opts,args
    for opt, arg in opts:
       print opt, arg
       if opt == '-h':
         sys.exit()
       elif opt in ["-s", "--start"]:
        start = int(arg)
       elif opt in ["-e", "--end"]:
         end = int(arg)
       elif opt in ["-c", "--crawldomain"]:
         crawldomain = arg
       elif opt in ["-d","--outputdir"]:
         outputdir = arg
       elif opt in ["-u", "--exclude-urls"]:
         excludeurls = arg

    cleanhtml='/'.join([outputdir,'cleanhtml.out'])
    NerParseResult='/'.join([outputdir,'parse.out'])

    if start<=1 and end>=1:
        subprocess.call(['wget', '-S', '-r', crawldomain])
#from html extract title, datestamp
    if start<=2 and end>=2:
        cmd = ' '.join(["find", crawldomain, "-name", "\"*\"", ">", "totalurls.txt" ])
        subprocess.call(cmd, shell=True)
        with open(excludeurls,'r') as f:
            excludeurlset = f.read()
        subprocess.call(['rm','-f',cleanhtml])    
        for file in open("totalurls.txt",'r'):
            if file not in excludeurlset:
		cmd = ' '.join(['python', '/'.join([execdir,'clean-html.py']), file.strip('\r\t\n'), 'title','>>', cleanhtml])
                print "running ",cmd
                subprocess.call(cmd, shell=True)
    if start<=3 and end>=3:
        cmd = ' '.join(['sh', '/'.join([execdir,'run-stanfordner.sh']), cleanhtml, '1>', NerParseResult])
        print "running step 3: ",cmd
        subprocess.call(cmd, shell=True)
    if start<=4 and end>=4:
        cmd =  ' '.join(['cat', NerParseResult, '|', 'python', '/'.join([execdir,'entity-extract-stanford.py']), '>', 'ner.txt'])
        print "running ",cmd
        subprocess.call(cmd, shell=True)

    if start<=5 and end>=5:
        cmd = ' '.join(['python', '/'.join([execdir,'format2.py']), 'ner.txt', cleanhtml, 'term.txt','context.txt'])
	print "running: ",cmd
        subprocess.call(cmd, shell=True)            
  


if __name__ == "__main__":
   main(sys.argv[1:])
