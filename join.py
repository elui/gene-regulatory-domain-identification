#!/usr/bin/python

import sys
import csv

def Rewind(index, start, lines2, strand, chrom):
    while True:
        if index <= 0:
            break
        if index >= len(lines2):
            break

        if not "mm9" in lines2[index][0] and not "hg18" in lines2[index][0]:
            chrom2 = lines2[index][0]
            #print "start: " + str(start) + "cur: " + lines2[index][6]
            #print chrom +  " " + chrom2
            if strand == '+' and (start > int(lines2[index][6]) or chrom < chrom2):
                break
            if strand == '-' and (start < int(lines2[index][7]) or chrom > chrom2):
                break

        if strand == '+':
            index -= 1
        else:
            index += 1

    return index

'''
Look for gene corresponding to transcription start sites

the for loop is repeated 3 times because on mm9, perfect matches were not found always
so the second two loops look for start sites that fall in the range of a gene, and names that are equal
'''
def merge(lines, lines2, ignore_strand):
    f2index = 2
    for i in xrange(len(lines)):

        n1 = lines[i][4]
        start1 = int(lines[i][2])

        if ignore_strand == lines[i][3]:
            continue

        chrom = lines[i][1]
        
        found = False

        oldI = f2index
        f2index = Rewind(f2index, start1, lines2, lines[i][3], chrom)

        for k in xrange(len(lines2) - f2index):
            index = k + f2index

            if "hg18" in lines2[index][0]:
                continue
            if "mm9" in lines2[index][0]:
                continue

            start2 = int(lines2[index][6])
            if (ignore_strand == '+'):
                start2 = int(lines2[index][7])

            start = int(lines2[index][1])
            end = int(lines2[index][2])

            starttx = int(lines2[index][6])
            endtx = int(lines2[index][7])

            chrom2 = lines2[index][0]

            if (chrom != chrom2):
                continue

            n2 = lines2[index][4]

            if (start1 == start2):
                print "%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s" % (lines[i][0], lines[i][1], lines[i][2], lines[i][3], lines[i][4], start, end, "match")
                f2index = index
                found = True
         
                break
        

        if found:
            continue
        for k in xrange(len(lines2) - f2index):
            index = k + f2index

            if "hg18" in lines2[index][0]:
                continue
            if "mm9" in lines2[index][0]:
                continue
            ##print str(index) + " : " + str(len(lines2))
            ##print lines2[index]
            #print index

            start2 = int(lines2[index][6])
            if (ignore_strand == '+'):
                start2 = int(lines2[index][7])

            start = int(lines2[index][1])
            end = int(lines2[index][2])

            starttx = int(lines2[index][6])
            endtx = int(lines2[index][7])

            chrom2 = lines2[index][0]

            if (chrom != chrom2):
                continue

            n2 = lines2[index][4]
            
            if (min(start,starttx) <= start1 and max(end,endtx) >= start1):
                print "%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s" % (lines[i][0], lines[i][1], lines[i][2], lines[i][3], lines[i][4], start, end, "range")
                f2index = index
                found = True
                break
            

        if found:
            continue
        for k in xrange(len(lines2) - f2index):
            index = k + f2index

            if "hg18" in lines2[index][0]:
                continue
            if "mm9" in lines2[index][0]:
                continue

            start2 = int(lines2[index][6])
            if (ignore_strand == '+'):
                start2 = int(lines2[index][7])

            start = int(lines2[index][1])
            end = int(lines2[index][2])

            starttx = int(lines2[index][6])
            endtx = int(lines2[index][7])

            chrom2 = lines2[index][0]

            if (chrom != chrom2):
                continue

            n2 = lines2[index][4]

            
            if (n1 == n2):
                print "%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s" % (lines[i][0], lines[i][1], lines[i][2], lines[i][3], lines[i][4], start, end, "name")
                f2index = index
                found = True
                break
        

        if not found:
            print "missing: " + n1 + " " + chrom + " " + str(start1) + " " + ignore_strand


def main():
    if len(sys.argv) < 4:
        print "Combines Isoforms in bed file"
        print "Usage: ./join.py [loci.bed] [genes.bed] [genes.bed.sorted2]"
        exit(1)

    filename = sys.argv[1]
    f = open(filename, 'r') 
    l1 = list(csv.reader(f, delimiter='\t'))
    f.close()

    filename2 = sys.argv[2]
    f = open(filename2, 'r') 
    l2 = list(csv.reader(f, delimiter='\t'))
    f.close()

    merge(l1, l2, '-')

    filename3 = sys.argv[3]
    #sortFile(filename2, filename3)
    f = open(filename3, 'r') 
    l3 = list(csv.reader(f, delimiter='\t'))
    f.close()

    merge(l1, l3, '+')


if __name__ == "__main__":
    main()