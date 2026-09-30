# count

Collect sgRNA read counts from raw sequencing files and write a count table.
Accepts FASTQ, gzipped FASTQ, and SAM/BAM input, and handles screens with UMIs
and paired-guide (dual-sgRNA) libraries.

Outputs `[prefix].count.txt` and `[prefix].countsummary.txt`; paired-guide runs
additionally write `[prefix].pg_count.txt`. See [file formats](../FILE_FORMATS.md#count-outputs)
for the column layouts.

```{eval-rst}
.. argparse::
   :module: mageck2.argsParser
   :func: build_parser
   :prog: mageck2
   :path: count
```

## See also

- [Tutorial 2 — starting from raw FASTQ files](../TUTORIAL.md#2-starting-from-raw-fastq-files)
- [Tutorial 6 — counting screens with UMIs](../TUTORIAL.md#6-counting-screens-with-umis)
- [Tutorial 7 — counting paired-guide screens](../TUTORIAL.md#7-counting-paired-guide-dual-sgrna-screens),
  which covers how to find the window the `--pg-start-2`/`--pg-end-2` options need
- [sgRNA library file format](../FILE_FORMATS.md#sgrna-library-file---list-seq)
