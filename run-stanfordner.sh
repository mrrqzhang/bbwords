#execdir=/tmp/ruiqiang/git_mrrqzhang/bbwords
#stanford=/tmp/ruiqiang/stanfordNER/stanford-ner-2015-04-20

input=$1
step=2000

execdir=/home/ruiqiang/Filers/ss05_ruiqiang/bombwords/git_mrrqzhang/bbwords
stanford=/home/ruiqiang/tools/stanford-ner-2015-04-20

for (( i=0; i<=300; i++ )) 
do
    start=$(( $i*2000 ))
    end=$(( $start+$step ))
#    echo $start $end
    awk -v s=$start -v e=$end '{if(NR>=s && NR<e){if($0~/URLID/)printf "\n%s",$0; if($0~/TITLE/ || $0~/TEXT/)printf "\t%s",$0}}'  $input > tmp.txt
#    exit
    java -mx1500m -cp $stanford/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier $stanford/classifiers/english.all.3class.distsim.crf.ser.gz -textFile tmp.txt  

done
