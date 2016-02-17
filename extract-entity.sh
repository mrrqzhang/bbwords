execdir=/tmp/ruiqiang/bbword
stanford=/tmp/ruiqiang/stanfordNER/stanford-ner-2015-04-20

for file in `cat $1` ; do
    echo $file
#    wget $file -O html.out
    python $execdir/clean-html.py $file title >& cleanhtml.out
    cat cleanhtml.out | python $execdir/nechunker.py
#    java -mx1500m -cp $stanford/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier $stanford/classifiers/english.all.3class.distsim.crf.ser.gz -textFile cleanhtml.out |\
#    python $execdir/entity-extract-stanford.py 
done
