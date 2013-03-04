#!/usr/bin/python

import math
import sys
import readwig
import scipy.ndimage.filters

def get_mean(values):
	return float(sum(values)) / float(len(values))

def get_stddev(values):
	mean = get_mean(values)
	return math.sqrt(float(sum([(x - mean) * (x - mean) for x in values])) / float(len(values)))

def get_cut_points(values, offset=0):
	if len(values) == 0:
		return (offset, offset)
	threshold = 1e-2
	start = 0
	for i in xrange(len(values)):
		if values[i] <= threshold:
			start = i
			break
	end = len(values) - 1
	for i in xrange(len(values) - 1, -1, -1):
		if values[i] <= threshold:
			end = i
			break
	return (start + offset, end + offset)

def get_genes(loci_filename, chrom):
	loci_file = open(loci_filename, "r")
	forward_genes = []
	backward_genes = []
	for loci_line in loci_file:
		tokens = loci_line.split()
		gene = {}
		gene["id"] = int(tokens[0])
		gene["chrom"] = tokens[1]
		gene["pos"] = int(tokens[2])
		gene["strand"] = tokens[3]
		gene["name"] = tokens[4]
		if gene["chrom"] == chrom:
			if gene["strand"] == "+":
				forward_genes.append(gene)
			if gene["strand"] == "-":
				backward_genes.append(gene)
	return (forward_genes, backward_genes)

def get_reg_doms(genes, cons_values):
	reg_doms = []
	reg_dom_cur_start = 0
	for i in range(-1, len(genes)):
		# Break if we go out of range
		if i >= 0 and genes[i]["pos"] > len(cons_values):
			break
		# Start of range is site of current gene
		if i >= 0:
			range_start = genes[i]["pos"]
		# Or start of chromosome if this is before our first gene
		else:
			range_start = 0
		# End of range is site of next gene
		if i + 1 < len(genes) and genes[i + 1]["pos"] <= len(cons_values):
			range_end = genes[i + 1]["pos"]
		# Or end of our data if this is the last gene
		else:
			range_end = len(cons_values)
		range_cons_values = cons_values[range_start:range_end]
		reg_dom_cur_end, reg_dom_next_start = get_cut_points(range_cons_values, range_start)
		if i >= 0:
			reg_doms.append({"chrom": genes[i]["chrom"], \
			"start": reg_dom_cur_start, \
			"end": reg_dom_cur_end, \
			"name": genes[i]["name"], \
			"id": genes[i]["id"]})
		reg_dom_cur_start = reg_dom_next_start
	return reg_doms

def print_reg_doms(reg_doms):
	for reg_dom in reg_doms:
		print "%s\t%d\t%d\t%s\t%d" % (reg_dom["chrom"], reg_dom["start"], reg_dom["end"], reg_dom["name"], reg_dom["id"])

def main():
	sigma = 50
	if len(sys.argv) < 4:
		print "Calculates start and end of regulatory regions."
		print "Usage: ./getconsregdoms.py [genes.loci] [chrom] [chrN.wig]"
		exit(1)
	loci_filename = sys.argv[1]
	chrom = sys.argv[2]
	cons_filename = sys.argv[3]
	print >> sys.stderr, "Loading genes..."
	forward_genes, backward_genes = get_genes(loci_filename, chrom)
	print >> sys.stderr, "Loading conservation values..."
	raw_cons_values = readwig.read_wig(cons_filename)
	print >> sys.stderr, "Applying smoothing..."
	cons_values = scipy.ndimage.filters.gaussian_filter(raw_cons_values, sigma)
	print >> sys.stderr, "Computing regulatory regions..."
	reg_doms = get_reg_doms(forward_genes, cons_values) + get_reg_doms(backward_genes, cons_values)
	print >> sys.stderr, "Printing regulatory regions..."
	print_reg_doms(reg_doms)

if __name__ == "__main__":
	main()
