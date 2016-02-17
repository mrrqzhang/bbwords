
from bs4 import  BeautifulSoup

import sys
import re

#html_doc='japan-puts-defense-forces-alert-over-possible-n-160100804.html'

#html_doc='Barack_Obama'

if  len(sys.argv) <= 2: sys.exit(0)
html_doc = sys.argv[1]
type = sys.argv[2]

soup = BeautifulSoup(open(html_doc), 'html5lib')
if not soup: sys.stderr.out('input file error: %s\n' % html_doc) 

if type=='title' or type=='all':
	title = soup.find_all('title')
	for item in title:
#    		if item.attrs: continue # dictionary is not empty
    		outstr=''
    		for str in item.stripped_strings:
        		outstr = outstr + ' ' + str
#        sys.stdout.write('%s ' % str.encode('utf-8'))
    		outstr = re.sub('\[.*\]','',outstr)
    		sys.stdout.write('%s\n' % outstr.encode('utf-8'))

#	sys.stdout.write('\n\n')

if type=='all':
    tag = soup.find_all('p')

    for item in tag:
    	outstr=''
    	for str in item.stripped_strings:
        	outstr = outstr + ' ' + str 
#        sys.stdout.write('%s ' % str.encode('utf-8'))
    	outstr = re.sub('\[.*\]','',outstr)
    	sys.stdout.write('%s\n' % outstr.encode('utf-8'))
