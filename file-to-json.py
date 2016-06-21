import json
import sys
from mypythonlib import convert_json

tag=True if sys.argv[1]=='True' else False
data=[]
for line in sys.stdin:
    data.append(line.strip('\r\t\n').split('\t'))
sys.stdout.write(convert_json(data,tag))
