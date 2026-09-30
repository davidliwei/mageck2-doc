# Frequently asked questions

Migrated and updated from the legacy [MAGeCK Q&A](https://sourceforge.net/p/mageck/wiki/QA/).
Most MAGeCK answers apply to mageck2; commands below use the `mageck2` executable.
For more, join the [MAGeCK Google group](https://groups.google.com/g/mageck) or
open an [issue](https://github.com/davidliwei/mageck2/issues).

## Installation

**Q: After a `--user` install, `mageck2` reports "command not found".**

`pip` installs the `mageck2` and `RRA` programs into the environment's `bin`
directory, which may not be on your `PATH`. Find it and add it — see the
[installation troubleshooting section](INSTALL.md#troubleshooting-command-not-found).

**Q: I have several mageck installations and the wrong one runs.**

Use a fresh virtual environment (`python -m venv` or a conda environment) so the
`mageck2` on your `PATH` and its Python package come from the same place. Check
which executable is active with `which mageck2`.

## Running mageck2

**Q: How do I handle biological vs. technical replicates?**

Pool **technical** replicates of one sample by joining their FASTQ files with a
comma in `--fastq` (e.g. `--fastq s1_rep1.fastq,s1_rep2.fastq s2_rep1.fastq,s2_rep2.fastq`).
Treat **biological** replicates as separate samples so mageck2 can model their
variance — e.g. `mageck2 test -t treat_r1,treat_r2 -c ctrl_r1,ctrl_r2`.

**Q: Reads have a variable-length prefix before the sgRNA. How do I trim it?**

mageck2 determines the trimming length automatically (`--trim-5 AUTO`, the
default), even when it varies within a file. You may instead give explicit
lengths (`--trim-5 7,8`), or trim adapters beforehand with a tool such as
[cutadapt](https://cutadapt.readthedocs.io/).

**Q: Where are the per-sample statistics of my FASTQ files?**

`count` writes a `*.countsummary.txt` file with, per sample, total reads, mapped
reads, mapping percentage, zero-count sgRNAs, and the Gini index. The same numbers
appear in the `*.log` file (see [file formats](FILE_FORMATS.md#count-outputs)).

**Q: How do I judge sample quality?**

As rules of thumb for a good negative-selection sample: mapped reads should be
well over 60% of total reads, and few sgRNAs (<5%, ideally <1%) should have zero
counts. Positive-selection screens may legitimately have many zero-count sgRNAs.
For a fuller treatment of QC metrics see the
[MAGeCK-VISPR paper](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-015-0843-6).

**Q: mageck2 cannot read my library or control-sgRNA file, though it looks fine.**

This is usually a line-ending problem from editing the file in a spreadsheet
program on Windows. Re-save it as plain UTF-8 text with Unix line endings (open in
a plain-text editor and save), then retry.

**Q: `mle` uses more CPU than the `--threads` value I set.**

numpy/scipy (via MKL/OpenBLAS) parallelize matrix operations independently of
mageck2's own threads. To cap them, set the environment variable before running:

    export OMP_NUM_THREADS=1
    mageck2 mle ...

**Q: How do I run a paired analysis?**

Add `--paired` to `test`. The samples in `-t` and `-c` must be equal in number and
in matching order, so replicate *i* of treatment pairs with replicate *i* of
control:

    mageck2 test -k count.txt -t treatment_r1,treatment_r2 -c control_r1,control_r2 --paired

Paired mode treats the sgRNAs of each pair as independent, effectively doubling the
sgRNAs per gene. This boosts power when replicates are poorly correlated, but can
introduce false positives when they are highly correlated — use it selectively.

## Interpreting results

**Q: How do I tell whether the screen worked?**

First check that the sample statistics look healthy (above). Then look at
well-known genes: negative-selection screens should rank ribosomal genes and
common essential genes (e.g. MYC) near the top. A good confirmation is to run the
`pathway` command against MSigDB KEGG gene sets — seeing ribosome, spliceosome,
proteasome, and cell-cycle pathways enriched is a strong positive sign.

**Q: Very few genes pass my FDR cutoff (e.g. 0.1). Why, and what can I do?**

Libraries with few sgRNAs per gene, large numbers of comparisons, and mageck2's
deliberately stringent statistics can all make the FDR conservative. To increase
sensitivity: pre-filter genes you know are irrelevant (very low expression, or <4
targeting sgRNAs); supply known non-essential controls via `--control-sgrna` /
`--control-gene` for a better null distribution; and use `--paired` when your
replicates are paired.

**Q: What does `--control-sgrna` (or `--control-gene`) do?**

It tells mageck2 to build the RRA null distribution from your provided
non-essential controls instead of assuming every gene is non-essential — usually a
less conservative, more accurate estimate. With `--norm-method control`, the
normalization factor is also computed from the controls only. Provide one ID per
line; see [Tutorial 5](TUTORIAL.md#5-using-negative-control-sgrnas-or-genes) for a
worked example and caveats.

## Visualization and reports

**Q: How do I generate the analysis report?**

mageck2 emphasizes R Markdown reports. The `count` and `test` commands emit R /
R Markdown files alongside their results; render them with R (with the relevant
output files in the same directory), for example:

    Rscript <output_prefix>_summary.R

Keep intermediate files with `--keep-tmp` if a rendering step fails so you can
inspect or re-run it. (The legacy static PDF report path is being retired in
mageck2 in favor of R Markdown.)

## Getting more help

- Search or post in the [MAGeCK Google group](https://groups.google.com/g/mageck).
- Report bugs and request features in the
  [issue tracker](https://github.com/davidliwei/mageck2/issues) (documentation and
  demo issues belong in
  [mageck2-doc](https://github.com/davidliwei/mageck2-doc/issues) /
  [mageck2-demo](https://github.com/davidliwei/mageck2-demo/issues)).
