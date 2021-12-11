# mageck2-doc

[mageck2](https://github.com/davidliwei/mageck2) is a model-based analysis tool for CRISPR screens, developed by the [Wei Li lab](https://weililab.org) from Children's National Hospital/George Washington University. 



mageck2 inherits the following functions of MAGeCK for CRISPR screening analysis:

* Simple treatment vs. control analysis (via RRA) and multiple sample comparison analysis (via MLE);
* Processing raw fastq files (via MAGeCK count), raw count table, normalized count table (via MAGeCK RRA or MLE), or even sgRNA ranks (via RRA);
* Various normalization approaches including custom negative control guides/genes;
* Copy-number variation (CNV) correction with or without known CNV profiles of cells;


In addition, mageck2 implements the following new functions:

* Processing and analyzing CRISPR screens with UMIs;
* Processing and analyzing paired-guide CRISPR screens (two gRNAs in one vector);
* Paired sample analysis (RRA only);
* More complicated experimental design including time-series and drug treatment CRISPR screen using MAGeCK MLE;
* New and simple R markdown based visualization (the PDF visualization in MAGeCK will retire in mageck2);

**Note:** mageck2 is compatible with most functions in mageck. Therefore, if you know how to run mageck, you should have no problem with most mageck2 functions. The documentation of mageck can be found on [sourceforge](https://sourceforge.net/p/mageck/wiki/Home/).

mageck2 is part of the softwares and databases for functional genetic screens, which also include: 

* [MAGeCK](https://sourceforge.net/p/mageck), the earlier version of mageck2;
* [MAGeCK-VISPR](https://bitbucket.org/liulab/mageck-vispr), a comprehensive quality control, analysis and visualization workflow for CRISPR/Cas9 screens, which has also been integrated into MAGeCK and mageck2; 
* [MAGeCKFlute](https://bitbucket.org/liulab/mageckflute/src/master/), an integrative R analysis pipeline for pooled CRISPR functional genetic screens;
* [scMAGeCK](https://bitbucket.org/weililab/scmageck/src/master/), a computational model to identify genes associated with multiple expression phenotypes from CRISPR screening coupled with single-cell RNA sequencing data;
* [CRISP-view](http://crispview.weililab.org/), a database of public functional genetic screening datasets.

# Contents

## Installation

See [installation page](INSTALL.md) for more details.

## Demo

We provide a set of running examples for mageck2. See [mageck2-demo](https://github.com/davidliwei/mageck2-demo) for more details.

## Usage

See [Usage page](USAGE.md].


## File formats

## FAQ 

