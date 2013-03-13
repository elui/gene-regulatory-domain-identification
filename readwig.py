#!/usr/bin/python

import sys
import re
import gzip
import numpy

def read_wig(filename):
	
	f = gzip.open(filename, "rb")
	maxpos = 0
	for line in f:
		if "fixedStep" in line:
			maxpos = int(extract_field(line, "start"))
		else:
			maxpos += 1
	f.close()

	values = numpy.zeros(maxpos + 1)

	f = gzip.open(filename, "rb")
	pos = 0
	for line in f:
		if "fixedStep" in line:
			pos = int(extract_field(line, "start"))
		else:
			values[pos] = float(line)
			pos += 1
	f.close();

	return values


def extract_field(input, fieldname):
	match = re.search("%s=(\S+)" % fieldname, input)
	if match:
		return match.group(1)
	else:
		return None

def main():
	if len(sys.argv) < 2:
		print "Reads in a wig file"
		print "Usage: ./readwig.py [input.wigFix.gz]"
		exit(1)
	filename = sys.argv[1]
	values = read_wig(filename)
	print values

if __name__ == "__main__":
	main()

