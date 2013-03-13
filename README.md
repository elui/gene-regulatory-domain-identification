This project implements heuristics for regulatory region prediction based on PhastCons and PhyloP scores.

Tools
-----
 
**bedlengths.py**: Python library that provides a single function, `readwig`, that converts in a fixed-step Wiggle file into a numpy array.

**getconsregdoms.py**: Command-line tool that produces a BED file of predicted regulatory regions, given a file of gene loci, chromosome number, and a Wiggle file of phastCons / phyloP scores. The heuristic for predicting a regulatory region for a gene start site is the following:

1. Perform a Gaussian filter over the conservation scores. The default sigma for the filter is 50.
2. Compute basal region to be 5kb upstream and 1kb downstream from the start site.
3. Extend the start of the basal upstream until the conservation score at the position is smaller than the cutoff. Extend the end of the basal region downstream while the conservation score at the end is greater than the conservation score at the position is smaller than the cutoff. The default cutoff is 0.01.
4. Compute the extended region. The extended region extends from end of the previous basal region to the start of the next basal region, or 1000kb from the basal region, whichever region is smaller.

**difftsv.py**: Command-line tool that compares all the two GREAT output files in TSV format, and computes new terms, deleted terms, and terms with differing p-value.

Results
-------

**hg18.sigma.25.curatedRegDoms**: Predicted regulatory domains for hg18 SRF using phastCons with sigma = 25, cutoff = 0.01.

**hg18.sigma.25.results.txt**: New terms, deleted terms and terms with differing p-value for hg18 SRF using phastCons with sigma = 25, cutoff = 0.01.

**hg18.sigma.50.curatedRegDoms**: Predicted regulatory domains for hg18 SRF using phastCons with sigma = 50, cutoff = 0.01.

**hg18.sigma.50.results.txt**: New terms, deleted terms and terms with differing p-value for hg18 SRF using phastCons with sigma = 50, cutoff = 0.01.

**hg18.sigma.100.curatedRegDoms**: Predicted regulatory domains for hg18 SRF using phastCons with sigma = 100, cutoff = 0.01.

**hg18.sigma.100.results.txt**: New terms, deleted terms and terms with differing p-value for hg18 SRF using phastCons with sigma = 100, cutoff = 0.01.

**mm9.phastCons.curatedRegDoms**: Predicted regulatory domains for mm9 p300 using phastCons with sigma = 100, cutoff = 0.01.

**mm9.phastCons.results.txt**: New terms, deleted terms and terms with differing p-value for mm9 p300 using phastCons with sigma = 50, cutoff = 0.01.

**mm9.phyloP.curatedRegDoms**: Predicted regulatory domains for mm9 p300 using phastCons with sigma = 100, cutoff = 0.01.

**mm9.phyloP.results.txt**: New terms, deleted terms and terms with differing p-value for mm9 p300 using phyloP with sigma = 50, cutoff = 0.01.
