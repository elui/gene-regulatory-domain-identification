#!/bin/bash

set -x

for i in {1..22}
do
	python getconsregdoms.py ontologies/hg18/hg18.loci chr$i phastCons28way/chr$i.pp.gz > tmp/hg18/chr$i.regDoms.bed
done

python getconsregdoms.py ontologies/hg18/hg18.loci chrX phastCons28way/chrX.pp.gz > tmp/hg18/chrX.regDoms.bed
python getconsregdoms.py ontologies/hg18/hg18.loci chrY phastCons28way/chrY.pp.gz > tmp/hg18/chrY.regDoms.bed
python getconsregdoms.py ontologies/hg18/hg18.loci chrM phastCons28way/chrM.pp.gz > tmp/hg18/chrM.regDoms.bed

cat tmp/hg18/*.regDoms.bed | sort -k1,1 -k2,2n > input/hg18/cons/hg18.curatedRegDoms
