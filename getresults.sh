#!/bin/bash

# set -x

if [ "$#" -ne "1" ]
then
	echo "Usage: ./getresults.sh [hg18 or mm9]"
	exit 1
fi
for file in GOBiologicalProcess.tsv GOCellularComponent.tsv GOMolecularFunction.tsv MGIExpressionDetected.tsv MGIPhenotype.tsv
do
	echo $file
	python difftsv.py output/$1/curated/$file output/$1/cons/$file
done
