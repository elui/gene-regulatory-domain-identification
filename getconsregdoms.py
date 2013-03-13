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
	genes = []
	for loci_line in loci_file:
		tokens = loci_line.split()
		gene = {}
		gene["id"] = int(tokens[0])
		gene["chrom"] = tokens[1]
		gene["pos"] = int(tokens[2])
		gene["strand"] = tokens[3]
		gene["name"] = tokens[4]
		if gene["chrom"] == chrom:
			genes.append(gene)
	return genes

def get_cutoff_point(cons_values, pos, cutoff, step):
	while pos >= 0 and pos < len(cons_values) and cons_values[pos] >= cutoff:
		pos += step
	return pos

def get_reg_doms(genes, cons_values):
	cutoff = 0.01
	base_upstream = 5000
	base_downstream = 1000
	distal = 1000000
	reg_doms = []
	reg_dom_cur_start = 0
	base_regions = [None] * len(genes);
	for i in range(0, len(genes)):
		if genes[i]["strand"] == "+":
			base_region_start = max(genes[i]["pos"] - base_upstream, 0)
			base_region_end = min(genes[i]["pos"] + base_downstream, len(cons_values) - 1)
		elif genes[i]["strand"] == "-":
			base_region_start = max(genes[i]["pos"] - base_downstream, 0)
			base_region_end = min(genes[i]["pos"] + base_upstream, len(cons_values) - 1)
		base_regions[i] = (base_region_start, base_region_end)

	cons_regions = [None] * len(genes)
	for i in range(0, len(genes)):
		cons_region_start = get_cutoff_point(cons_values, base_regions[i][0], cutoff, -1)
		cons_region_end = get_cutoff_point(cons_values, base_regions[i][1], cutoff, 1)
		cons_regions[i] = (cons_region_start, cons_region_end)


	reg_regions = [None] * len(genes)
	for i in range(0, len(genes)):
		if i == 0:
			reg_region_start = max(0, cons_regions[i][0] - distal)
		else:
			reg_region_start = min(cons_regions[i][0], max(cons_regions[i - 1][1], cons_regions[i][0] - distal))

		if i == len(genes) - 1:
			reg_region_end = min(len(cons_values) - 1, cons_regions[i][1] + distal)
		else:
			reg_region_end = max(cons_regions[i][1], min(cons_regions[i + 1][0], cons_regions[i][1] + distal))
		reg_regions[i] = (reg_region_start, reg_region_end)

	reg_doms = [None] * len(genes)
	for i in range(0, len(genes)):
		reg_doms[i] = {"chrom": genes[i]["chrom"], \
			"start": reg_regions[i][0], \
			"end": reg_regions[i][1], \
			"name": genes[i]["name"], \
			"id": genes[i]["id"]}
	return reg_doms

# 	reg_doms.append({"chrom": genes[i]["chrom"], \
		# 	"start": reg_dom_cur_start, \
		# 	"end": reg_dom_cur_end, \
		# 	"name": genes[i]["name"], \
		# 	"id": genes[i]["id"]})

		# # Break if we go out of range
		# if i >= 0 and genes[i]["pos"] > len(cons_values):
		# 	break
		# # Start of range is site of current gene
		# if i >= 0:
		# 	range_start = genes[i]["pos"]
		# # Or start of chromosome if this is before our first gene
		# else:
		# 	range_start = 0
		# # End of range is site of next gene
		# if i + 1 < len(genes) and genes[i + 1]["pos"] <= len(cons_values):
		# 	range_end = genes[i + 1]["pos"]
		# # Or end of our data if this is the last gene
		# else:
		# 	range_end = len(cons_values)
		# range_cons_values = cons_values[range_start:range_end]
		# reg_dom_cur_end, reg_dom_next_start = get_cut_points(range_cons_values, range_start)
		# if i >= 0:
		# 	reg_doms.append({"chrom": genes[i]["chrom"], \
		# 	"start": reg_dom_cur_start, \
		# 	"end": reg_dom_cur_end, \
		# 	"name": genes[i]["name"], \
		# 	"id": genes[i]["id"]})
		# reg_dom_cur_start = reg_dom_next_start
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
	genes = get_genes(loci_filename, chrom)
	print >> sys.stderr, "Loading conservation values..."
	raw_cons_values = readwig.read_wig(cons_filename)
	print >> sys.stderr, "Applying smoothing..."
	cons_values = scipy.ndimage.filters.gaussian_filter(raw_cons_values, sigma)
	print >> sys.stderr, "Computing regulatory regions..."
	reg_doms = get_reg_doms(genes, cons_values)
	print >> sys.stderr, "Printing regulatory regions..."
	print_reg_doms(reg_doms)

if __name__ == "__main__":
	main()
