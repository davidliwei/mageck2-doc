# File formats

This page describes the input and output files used by mageck2. Runnable
examples of every file below are available in the
[mageck2-demo](https://github.com/davidliwei/mageck2-demo) repository.

All tabular files are **tab-separated** unless noted otherwise. Column order
matters: mageck2 identifies the sgRNA and gene columns by position (1st and 2nd),
not by header name.

---

## Input files

### sgRNA library file (`--list-seq`)

Used by `count` to map reads to sgRNAs. A `csv` or `txt` file with three columns
and no required header: **sgRNA ID**, **sequence**, **gene**.

    s_10007	TGTTCACAGTATAGTTTGCC	CCNA1
    s_10008	TTCTCCCTAATTGCTTGCTG	CCNA1
    s_10027	ACATGTTGCTTCCCCTTGCA	CCNC

Provide an empty file to collect counts for all observed sequences. For
paired-guide screens, a second library is supplied with `--list-seq-2`.

### Count table (`-k` / `--count-table`)

The primary input to `test`, `mle`, and `plot`, and an alternative input to
`count`. First row is a header; first two columns are the **sgRNA** and **Gene**,
followed by one read-count column per sample:

    sgRNA	Gene	HL60.initial	KBM7.initial	HL60.final	KBM7.final
    A1CF_m52595977	A1CF	213	274	883	175
    A1CF_m52596017	A1CF	294	412	1554	1891

Sample labels in the header are what you pass to `-t`/`-c` (in `test`) or
`--include-samples` (in `mle`).

### Design matrix (`-d` / `--design-matrix`) {#design-matrix}

Used by `mle` to describe the experimental design. Tab-separated. The first
column (`Samples`) lists sample labels matching the count table; the remaining
columns are the model variables, with a required `baseline` column of all 1s.
Entries are 0/1:

    Samples	baseline	HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE	KBM7
    HL60.initial	1	0	0
    KBM7.initial	1	0	0
    HL60.final	1	1	0
    KBM7.final	1	0	1

The matrix may also be given inline as a quoted string, e.g. `-d "1,1;1,0"`
together with `--include-samples` and `--beta-labels`.

### Control sgRNA / gene list (`--control-sgrna`, `--control-gene`)

A plain text file with one sgRNA ID (or gene ID) per line. Used for
control-based normalization and for building the RRA null distribution.

### Pathway / gene-set file (`--gmt-file`)

Standard [GMT format](https://software.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats#GMT:_Gene_Matrix_Transposed_file_format_.28.2A.gmt.29):
one gene set per line — set name, description, then tab-separated gene symbols.
Used by `pathway` and by `count`'s negative-selection QC.

### CNV files (`--cnv-norm`, `--cnv-est`)

- `--cnv-norm`: a tab-separated matrix of copy-number values, one gene per row
  and one cell line per column, used to correct CNV-biased scores. The first
  column header **must** be literally `SYMBOL` (mageck2 looks up gene ids by that
  name); the remaining headers are cell-line names, matched to `--cell-line` (or,
  for `mle`, to the design-matrix condition labels):

      SYMBOL	HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE	KBM7
      A1BG	0.1105	0.0433
      NAT2	0.0104	-0.2011
- `--cnv-est`: a BED file of gene positions, used to *estimate* CNV profiles
  directly from the screen data.

### sgRNA efficiency file (`--sgrna-efficiency`, `mle` only)

At least two columns: sgRNA ID and a predicted efficiency score. The column
indices are set with `--sgrna-eff-name-column` / `--sgrna-eff-score-column`
(0-based).

---

## Output files

All commands write a `[prefix].log` file (`-n`/`--output-prefix` sets the prefix,
default `sample1`).

### `count` outputs

- **`[prefix].count.txt`** — raw count table (same layout as the count-table
  input above): `sgRNA`, `Gene`, then one column per sample.
- **`[prefix].count_normalized.txt`** — normalized counts, same layout.
- **`[prefix].countsummary.txt`** — per-sample QC summary, one row per input
  file. Columns:

  | Column | Meaning |
  |---|---|
  | `File`, `Label` | input file and sample label |
  | `Reads`, `Mapped`, `Percentage` | total reads, mapped reads, mapping rate |
  | `TotalsgRNAs`, `Zerocounts` | sgRNAs in the library, sgRNAs with zero reads |
  | `GiniIndex` | evenness of sgRNA read distribution |
  | `NegSelQC*` | negative-selection QC score, p-value, permutation p-value/FDR, and gene count (present when `--day0-label` is used) |

### `test` (RRA) outputs

- **`[prefix].gene_summary.txt`** — gene-level results, with parallel
  negative- and positive-selection columns:

  | Column | Meaning |
  |---|---|
  | `id`, `num` | gene ID, number of sgRNAs |
  | `neg\|score`, `neg\|p-value`, `neg\|fdr`, `neg\|rank` | negative-selection RRA score, p-value, FDR, rank |
  | `neg\|goodsgrna`, `neg\|lfc` | # sgRNAs ahead of the alpha cutoff, gene log2 fold change |
  | `pos\|score` … `pos\|lfc` | the same set of columns for positive selection |

- **`[prefix].sgrna_summary.txt`** — sgRNA-level results. Columns include
  `sgrna`, `Gene`, `control_count`, `treatment_count`, `control_mean`,
  `treat_mean`, `LFC`, `control_var`, `adj_var`, `score`, `p.low`, `p.high`,
  `p.twosided`, `FDR`, and `high_in_treatment`.

- **`[prefix].normalized.txt`** — normalized counts (only with
  `--normcounts-to-file`).

### `mle` outputs

- **`[prefix].gene_summary.txt`** — one block of columns per condition (variable)
  in the design matrix: `Gene`, `sgRNA`, then for each condition
  `<condition>|beta`, `|z`, `|p-value`, `|fdr`, `|wald-p-value`, `|wald-fdr`. The
  **beta score** is the estimated selection effect (negative = depleted /
  essential, positive = enriched).
- **`[prefix].sgrna_summary.txt`** — `Gene`, `sgRNA`, `eff` (estimated sgRNA
  efficiency).

### `pathway` outputs

A pathway/gene-set enrichment summary (`[prefix].pathway_summary.txt`) reporting,
for each gene set, its enrichment statistic, p-value, and FDR in the tested
direction(s). The exact columns depend on `--method` (`gsea` or `rra`).

### `plot` outputs

Per-gene graphics (and an accompanying report) for the genes given in `--genes`.

---

See [USAGE.md](USAGE.md) for the command that produces each file, and the
[mageck2-demo](https://github.com/davidliwei/mageck2-demo) repository for
complete, runnable examples.
