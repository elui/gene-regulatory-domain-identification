This project implements heuristics for regulatory region prediction based on PhastCons and PhyloP scores.

Tools
-----
 
**bedlengths.py**: Python library that provides a single function, `readwig`, that converts in a fixed-step Wiggle file into a numpy array.

**getconsregdoms.py**: Command-line tool that produces a BED file of predicted regulatory regions, given a file of gene loci, chromosome number, and a Wiggle file of phastCons / phyloP scores.

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
