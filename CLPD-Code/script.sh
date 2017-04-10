if [ $2 = 'Jaccard' ]; then
	python jaccard.py $1 $2
else
	python clpd_asa.py $1 $2
fi;
python ../data/precision.py $1 $2