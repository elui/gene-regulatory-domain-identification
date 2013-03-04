#!/usr/bin/python

import sys

# Reads in items in BED format, and prints their lengths
def main():
	for line in sys.stdin:
		if line:
			tokens = line.split()
			start = int(tokens[1])
			end = int(tokens[2])
			length = end - start
			print length

if __name__ == "__main__":
	main()
