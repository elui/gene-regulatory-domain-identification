#!/usr/bin/python

import sys
import operator

def read_tsv(filename):
	f = open(filename, "r")
	entries = {}
	for line in f:
		if line[0] == "#":
			continue
		tokens = line.split("\t")
		desc = tokens[1]
		p_value = float(tokens[4])
		entries[desc] = p_value
	return entries

def get_difference(entries_1, entries_2):
	keys = set(entries_1.keys()) - set(entries_2.keys())
	entries = [(key, entries_1[key]) for key in keys]
	return sorted(entries, key=operator.itemgetter(1), reverse=True)

def get_modified(entries_1, entries_2):
	keys = set(entries_1.keys()) & set(entries_2.keys())
	entries = []
	for key in keys:
		if entries_1[key] != entries_2[key]:
			entries.append((key, entries_2[key] - entries_1[key]))
	return sorted(entries, key=operator.itemgetter(1), reverse=True)

def print_entries(entries):
	for entry in entries:
		if entry:
			print "%s\t%e" % (entry[0], entry[1])

def main():
	max_items = 10
	if len(sys.argv) < 3:
		print "Diffs two TSV files."
		print "Usage: ./difftsv.py [1.tsv] [2.tsv]"
		exit(1)
	filenames = sys.argv[1:3]
	tsv_entries = [read_tsv(filename) for filename in filenames]
	print ""
	print "Deleted entries:"
	print_entries(get_difference(tsv_entries[0], tsv_entries[1]))
	print ""
	print "Inserted entries:"
	print_entries(get_difference(tsv_entries[1], tsv_entries[0]))
	print ""
	print "Changed entries:"
	print_entries(get_modified(tsv_entries[0], tsv_entries[1]))
	print ""

if __name__ == "__main__":
	main()
