# Usage

MAGeCK2 is a single command with five subcommands:

```{list-table}
:header-rows: 1
:widths: 12 88

* - Subcommand
  - Purpose
* - [`count`](count.md)
  - Collect sgRNA read counts from FASTQ (or SAM/BAM) files, including screens
    with UMIs and paired-guide screens.
* - [`test`](test.md)
  - Rank sgRNAs and genes from a count table using Robust Rank Aggregation
    (RRA), comparing treatment against control.
* - [`mle`](mle.md)
  - Estimate gene essentiality (beta scores) by maximum likelihood under an
    experimental design matrix.
* - [`pathway`](pathway.md)
  - Test gene sets for enrichment in a gene ranking.
* - [`plot`](plot.md)
  - Draw per-gene figures from a count table and a `test` gene summary.
```

Every option on these pages is read directly from the installed MAGeCK2's
argument parser when the documentation is built, so it describes the version
shown in the sidebar rather than whatever was true when the page was written.
Running `mageck2 <subcommand> --help` gives you the same text.

```{toctree}
:hidden:

count
test
mle
pathway
plot
```
