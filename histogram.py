#!/usr/bin/python

import sys

# Reads a series of numbers, one on each line, then prints the maximum number
def main():
	if len(sys.argv) != 2:
		print("Usage: ./histogram.py [binSize]")
	bin_size = int(sys.argv[1])
	max_bin = 0
	counts = {}
	for line in sys.stdin:
		if line:
			x = int(line)
			bin = x / bin_size
			if bin not in counts:
				counts[bin] = 0
			counts[bin] += 1
			if max_bin < bin:
				max_bin = bin
	for i in range(max_bin + 1):
		bin_label = i * bin_size
		if i in counts:
			print "%d\t%d" % (bin_label, counts[i])
		else:
			print "%d\t0" % bin_label

if __name__ == "__main__":
	main()
