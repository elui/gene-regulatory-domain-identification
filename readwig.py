#!/usr/bin/python

import sys
import re

def read_wig(filename):
	f = open(filename, "r")
	values = []
	pos = 0
	for line in f:
		if "fixedStep" in line:
			start = int(extract_field(line, "start"))
			if len(values) <= start:
				values += [0] * (start - len(values) - 1)
		else:
			values.append(float(line))
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
		print "Usage: ./readwig.py [input.wigFix]"
		exit(1)
	filename = sys.argv[1]
	print read_wig(filename)

if __name__ == "__main__":
	main()

