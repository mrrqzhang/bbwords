import html5lib
from bs4 import  BeautifulSoup

import sys
import re
import random
import string


#html_doc='japan-puts-defense-forces-alert-over-possible-n-160100804.html'

#html_doc='Barack_Obama'

if  len(sys.argv) <= 2: sys.exit(0)
html_doc = sys.argv[1]
type = sys.argv[2]

try:
     soup = BeautifulSoup(open(html_doc), 'html5lib')
except: 
	sys.stderr.write('input file error: %s\n' % html_doc)
	sys.exit(0)

random = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
sys.stdout.write('URLID%s:\t%s\n' % (random,html_doc) )

if type=='title' or type=='all':
	title = soup.find_all('title')
	tstr=''
	for item in title:
    		outstr=''
    		for str in item.stripped_strings:
        		outstr = outstr + ' ' + str
    		outstr = re.sub('\[.*\]','',outstr)
                tstr = tstr+outstr+' '
                break						#only output one title if multiples
    	sys.stdout.write('TITLE:\t%s\n' % tstr.encode('utf-8'))

if type=='time' or type=='title' or type=='all':
	timetag = soup.find_all(property="article:published_time")
	
        for item in timetag:
            time = re.search('(.+)T(.+)-.*', item['content'])
	    sys.stdout.write('DATE:\t%s\n' % time.group(1).encode('utf-8'))
            sys.stdout.write('TIME:\t%s\n' % time.group(2).encode('utf-8'))
	    break  #only use one time
        if not timetag: 
            sys.stdout.write('DATE:\nTIME:\n')


if type=='all':
    tag = soup.find_all('p')
    tstr=''
    for item in tag:
    	outstr=''
    	for str in item.stripped_strings:
        	outstr = outstr + ' ' + str 
#        sys.stdout.write('%s ' % str.encode('utf-8'))
    	outstr = re.sub('\[.*\]','',outstr)
	tstr = tstr+outstr+' '
    sys.stdout.write('TEXT:\t%s\n' % tstr.encode('utf-8'))


   






