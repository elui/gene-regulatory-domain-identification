#!/bin/bash

set -x

for i in {1..19}
do
	python getconsregdoms.py ontologies/mm9/mm9.loci chr$i phastCons28way/chr$i.placental.pp.data.gz > tmp/mm9/chr$i.regDoms.bed
done

python getconsregdoms.py ontologies/mm9/mm9.loci chrX phastCons28way/chrX.placental.pp.data.gz > tmp/mm9/chrX.regDoms.bed
python getconsregdoms.py ontologies/mm9/mm9.loci chrY phastCons28way/chrY.placental.pp.data.gz > tmp/mm9/chrY.regDoms.bed
python getconsregdoms.py ontologies/mm9/mm9.loci chrM phastCons28way/chrM.placental.pp.data.gz > tmp/mm9/chrM.regDoms.bed

cat tmp/mm9/*.regDoms.bed | sort -k1,1 -k2,2n > input/mm9/cons/mm9.curatedRegDoms
