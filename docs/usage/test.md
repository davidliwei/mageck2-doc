# test

Given a count table — from the [`count`](count.md) command or your own — rank
sgRNAs and genes using the Robust Rank Aggregation (RRA) algorithm, comparing
treatment against control samples.

Outputs `[prefix].gene_summary.txt` and `[prefix].sgrna_summary.txt`; see
[file formats](../FILE_FORMATS.md#test-rra-outputs).

```{eval-rst}
.. argparse::
   :module: mageck2.argsParser
   :func: build_parser
   :prog: mageck2
   :path: test
```

## See also

- [Tutorial 1 — RRA analysis from a read count table](../TUTORIAL.md#1-rra-analysis-from-a-read-count-table)
- [Tutorial 5 — using negative-control sgRNAs or genes](../TUTORIAL.md#5-using-negative-control-sgrnas-or-genes)
- [Tutorial 8 — correcting copy-number variation effects](../TUTORIAL.md#8-correcting-copy-number-variation-cnv-effects)
- [Interpreting the results](../FAQ.md#interpreting-results)
