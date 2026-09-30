# MAGeCK2

[MAGeCK2](https://github.com/davidliwei/mageck2) is a model-based analysis tool
for CRISPR screens, developed by the [Wei Li lab](https://weililab.org) at the
University of Maryland School of Medicine and the University of Maryland
Institute for Health Computing.

MAGeCK2 inherits the following functions of MAGeCK for CRISPR screening analysis:

* Simple treatment vs. control analysis (via RRA) and multiple sample comparison
  analysis (via MLE);
* Processing raw FASTQ files (via `count`), raw count tables, normalized count
  tables (via `test` or `mle`), or even sgRNA ranks (via RRA);
* Various normalization approaches including custom negative control
  guides/genes;
* Copy-number variation (CNV) correction with or without known CNV profiles of
  cells.

In addition, MAGeCK2 implements the following new functions:

* Processing and analyzing CRISPR screens with UMIs;
* Processing and analyzing paired-guide CRISPR screens (two gRNAs in one vector);
* Paired sample analysis (RRA only);
* More complicated experimental designs including time-series and
  drug-treatment CRISPR screens using MAGeCK MLE;
* New and simple R-markdown-based visualization (the PDF visualization in MAGeCK
  will retire in MAGeCK2).

:::{note}
MAGeCK2 is compatible with most functions in MAGeCK. If you know how to run
MAGeCK, you should have no problem with most MAGeCK2 functions. The
documentation of MAGeCK can be found on
[SourceForge](https://sourceforge.net/p/mageck/wiki/Home/).
:::

## Getting started

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} {octicon}`download` Installation
Install from PyPI or from source, and check that the compiled helpers are on
`PATH`.

+++
[Installation](INSTALL.md)
:::

:::{grid-item-card} {octicon}`book` Tutorials
Eleven step-by-step walkthroughs, from a count table to paired-guide screens and
complex designs.

+++
[Tutorials](TUTORIAL.md)
:::

:::{grid-item-card} {octicon}`terminal` Command-line reference
Every option of every subcommand, generated from MAGeCK2's own argument parser.

+++
[Usage](usage/index.md)
:::

:::{grid-item-card} {octicon}`file` File formats
The layout of every input and output file MAGeCK2 reads or writes.

+++
[File formats](FILE_FORMATS.md)
:::

::::

Runnable example datasets and scripts live in a separate repository,
[mageck2-demo](https://github.com/davidliwei/mageck2-demo).

## The MAGeCK family

MAGeCK2 is part of a set of software and databases for functional genetic
screens, which also includes:

* [MAGeCK](https://sourceforge.net/p/mageck), the earlier version of MAGeCK2;
* [MAGeCK-VISPR](https://bitbucket.org/liulab/mageck-vispr), a comprehensive
  quality control, analysis and visualization workflow for CRISPR/Cas9 screens,
  which has also been integrated into MAGeCK and MAGeCK2;
* [MAGeCKFlute](https://bitbucket.org/liulab/mageckflute/src/master/), an
  integrative R analysis pipeline for pooled CRISPR functional genetic screens;
* [scMAGeCK](https://bitbucket.org/weililab/scmageck/src/master/), a
  computational model to identify genes associated with multiple expression
  phenotypes from CRISPR screening coupled with single-cell RNA sequencing;
* [CRISP-view](http://crispview.weililab.org/), a database of public functional
  genetic screening datasets.

## Repositories

* [mageck2](https://github.com/davidliwei/mageck2) — source code and issue tracker
* [mageck2-demo](https://github.com/davidliwei/mageck2-demo) — runnable example datasets and workflows
* [mageck2-doc](https://github.com/davidliwei/mageck2-doc) — the source of this documentation

```{toctree}
:hidden:
:maxdepth: 2

INSTALL
TUTORIAL
usage/index
FILE_FORMATS
FAQ
```
