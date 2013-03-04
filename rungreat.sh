#!/bin/bash

set -x

if [ "$#" -ne "2" ]
then
	echo "Usage: ./rungreat.sh [hg18 or mm9] [curated or cons]"
	exit 1
fi

if [ "$1" = "hg18" ]
then
	dataset="SRF.hg18.bed"
elif [ "$1" = "mm9" ]
then
	dataset="p300Limb.mm9.bed"
else
	echo "Error: Unknown genome"
	exit 1
fi

# Remove old files
rm ontologies/$1/$1.curatedRegDoms output/$1/$2/*

# Copy input file
cp input/$1/$2/$1.curatedRegDoms ontologies/$1/$1.curatedRegDoms

# Run great
./GREAT $1 $dataset ontologies/$1 output/$1/$2/
