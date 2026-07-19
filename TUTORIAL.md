# Tutorials

These tutorials walk through common mageck2 workflows. Most correspond to a folder
in the [mageck2-demo](https://github.com/davidliwei/mageck2-demo) repository that
contains the input data and a `run.sh` script — clone that repo and run the
commands from inside the matching folder. Tutorials that use large public datasets
(3, 10, 11) download their own data.

**Prerequisite:** install mageck2 first (see [installation](INSTALL.md)). For the
input/output file layouts referenced here, see [file formats](FILE_FORMATS.md);
for the full option reference, see [usage](USAGE.md).

## Outline

**Basic analysis**

| # | Tutorial | What it covers |
|---|---|---|
| 1 | [RRA from a read count table](#1-rra-analysis-from-a-read-count-table) | The simplest treatment-vs-control test on an existing count table |
| 2 | [Starting from raw FASTQ files](#2-starting-from-raw-fastq-files) | `count` then `test` on a small toy dataset |
| 3 | [End-to-end with a public screening dataset](#3-end-to-end-analyzing-a-public-screening-dataset) | Download real FASTQ, prepare a library, count, test, and interpret hits |
| 4 | [Multi-condition analysis with MAGeCK MLE](#4-multi-condition-analysis-with-mageck-mle) | Beta scores across conditions using a design matrix |
| 5 | [Using negative-control sgRNAs or genes](#5-using-negative-control-sgrnas-or-genes) | Improve p-values and normalization with known controls |

**Counting special library types**

| # | Tutorial | What it covers |
|---|---|---|
| 6 | [Counting screens with UMIs](#6-counting-screens-with-umis) | Automatic UMI detection and per-UMI counts |
| 7 | [Counting paired-guide screens](#7-counting-paired-guide-dual-sgrna-screens) | Dual-sgRNA (combinatorial) vectors |

**Advanced analysis**

| # | Tutorial | What it covers |
|---|---|---|
| 8 | [Correcting copy-number variation (CNV) effects](#8-correcting-copy-number-variation-cnv-effects) | Remove amplification-driven false positives |
| 9 | [Complex experimental designs](#9-complex-experimental-designs) | Time-series and paired designs with MLE |
| 10 | [Mismatch-tolerant read mapping](#10-mismatch-tolerant-read-mapping) | Align with Bowtie2 and feed BAM to `count` |
| 11 | [Incorporating sgRNA efficiency](#11-incorporating-sgrna-efficiency) | Weight guides by predicted activity in MLE |

---

# Basic analysis

## 1. RRA analysis from a read count table

*(demo folder: `demo1_rra_from_count_table`)*

The simplest workflow: given a count table, compare treatment vs. control samples
and rank sgRNAs and genes with RRA. `sample.txt` has a header line
(`sgRNA  Gene  HL60.initial  KBM7.initial  HL60.final  KBM7.final`) and one row per
sgRNA.

    mageck2 test -k sample.txt -t HL60.final,KBM7.final -c HL60.initial,KBM7.initial -n demo

Samples may also be given by 0-based index, so the following is equivalent:

    mageck2 test -k sample.txt -t 2,3 -c 0,1 -n demo

This produces `demo.gene_summary.txt`, `demo.sgrna_summary.txt`, and `demo.log`.
In the gene summary, genes are ranked separately for negative selection
(`neg|*` columns, depleted in treatment) and positive selection (`pos|*` columns,
enriched); see [file formats](FILE_FORMATS.md#test-rra-outputs).

## 2. Starting from raw FASTQ files

*(demo folder: `demo2_run_mageck_from_fastq`)*

If you start from sequencing reads, first build a count table with `count`
(supplying an sgRNA library file), then run `test`:

    # 1. count reads against the library
    mageck2 count -l library.txt -n demo --sample-label L1,CTRL --fastq test1.fastq test2.fastq

    # 2. statistical test on the resulting count table
    mageck2 test -k demo.count.txt -t L1 -c CTRL -n demo

`count` also writes a `demo.countsummary.txt` QC file summarizing mapping rate,
zero-count sgRNAs, and the Gini index per sample. Join technical replicates of one
sample with a comma in `--fastq` (e.g.
`--fastq s1_rep1.fastq,s1_rep2.fastq s2_rep1.fastq,s2_rep2.fastq`).

> The old all-in-one `run` command has been discontinued; run `count` then `test`.

## 3. End-to-end: analyzing a public screening dataset

This tutorial goes the whole way from raw reads of a *public* screen to a ranked
gene list, using the mouse ESC essentiality screen of
[Koike-Yusa et al., Nat Biotechnol 2014](https://www.nature.com/articles/nbt.2800)
(ENA study `ERP003292`). It is the best way to learn the real pipeline.

### Step 1 — download the FASTQ files

Two runs: a plasmid reference and an ESC replicate.

    wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR376/ERR376998/ERR376998.fastq.gz
    wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR376/ERR376999/ERR376999.fastq.gz

mageck2 reads `.fastq.gz` directly, so you do **not** need to unzip them.

### Step 2 — prepare the sgRNA library file

Use the Yusa library that matches this screen. Ready-made libraries (including
`yusa_library.csv`) are on the
[MAGeCK libraries page](https://sourceforge.net/projects/mageck/files/libraries/);
alternatively, build the three-column library (sgRNA id, sequence, gene) from the
paper's supplementary table. See the
[library file format](FILE_FORMATS.md#sgrna-library-file---list-seq).

### Step 3 — determine the trimming length (usually automatic)

Since v0.5.6 mageck2 auto-detects the 5′ trim length (`--trim-5 AUTO`, the
default) and reads the sgRNA length from the library, so you can normally skip this
step. To set it manually, inspect the reads: in this dataset every read begins with
the same 23-nt vector sequence before the guide:

    CTTGTGGAAAGGACGAAACACCG[guide...]

so 23 nt should be trimmed (`--trim-5 23`). If the prefix length varies between
reads, trim adapters first with [cutadapt](https://cutadapt.readthedocs.io/).

### Step 4 — count reads against the library

    mageck2 count -l yusa_library.csv -n escneg --sample-label "plasmid,ESC1" \
        --fastq ERR376998.fastq.gz ERR376999.fastq.gz

Add `--trim-5 23` only if automatic detection fails. This writes
`escneg.count.txt` (and `escneg.countsummary.txt`). The count table looks like:

    sgRNA                     Gene            plasmid   ESC1
    chr19:5884430-5884453     SLC25A45        13        32
    chr11:58831475-58831498   OLFR312         94        108

Check `escneg.countsummary.txt` for the mapping rate and zero-count fraction before
moving on (see [judging sample quality](FAQ.md#interpreting-results)).

### Step 5 — test ESC vs. plasmid and interpret

    mageck2 test -k escneg.count.txt -t ESC1 -c plasmid -n esccp

The top **negatively selected** genes in `esccp.gene_summary.txt` are the ones
essential for ESC viability — ribosomal proteins such as `RPS5` and `RPL19` should
rank near the top, a good sign the screen worked. To find the top **positively
selected** genes, sort by the positive-selection rank column (column 12):

    sort -k 12,12n esccp.gene_summary.txt | head

In this screen `TRP53` (the mouse *TP53* homolog) is the strongest positively
selected gene. From here you can run [pathway enrichment](USAGE.md#pathway) or
[plot](USAGE.md#plot) individual genes.

## 4. Multi-condition analysis with MAGeCK MLE

*(demo folder: `demo3_mle_with_cnv_correction`)*

The MLE module estimates a single **beta score** per gene per condition, instead of
the separate positive/negative scores of `test`. A beta score behaves like a log
fold change: **negative = depleted / essential**, **positive = enriched**. Because
every condition is on the same scale, beta scores can be compared directly across
conditions and experiments, and the model can incorporate sgRNA efficiency
(Tutorial 11).

Conditions are described by a **design matrix**. `designmat.txt` is tab-separated:

    Samples         baseline    HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE    KBM7
    HL60.initial    1           0                                          0
    KBM7.initial    1           0                                          0
    HL60.final      1           1                                          0
    KBM7.final      1           0                                          1

Design-matrix rules:

- The first column (`Samples`) lists sample labels that match the count table.
- A required `baseline` column is `1` for every sample — the shared reference state.
- The remaining columns are the conditions you want beta scores for; entries are
  `0`/`1`.
- At least one initial/reference sample (day 0 or plasmid) should have `1` only in
  the `baseline` column.
- If more than one sample has `1` only in the `baseline` column (e.g. both
  `HL60.initial` and `KBM7.initial` above), they are **pooled** into a single
  shared reference — their average defines the baseline, and every beta is measured
  against it. MAGeCK does not treat them as separate cell lines. This assumes the
  initials share a common starting representation (here, the same library plasmid
  pool). If your references genuinely differ, run `mle` separately for each so each
  gets its own baseline.

Run MLE:

    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia --permutation-round 2

`beta_leukemia.gene_summary.txt` has, for each condition, a block of
`<condition>|beta`, `|z`, `|p-value`, `|fdr`, `|wald-p-value`, `|wald-fdr` columns
(see [file formats](FILE_FORMATS.md#mle-outputs)). `beta_leukemia.sgrna_summary.txt`
reports per-sgRNA efficiency.

## 5. Using negative-control sgRNAs or genes

*(demo folder: `demo5_use_control_guides`)*

By default mageck2 builds the RRA null distribution assuming all genes are
non-essential, which can be over-conservative. If you have known non-essential
controls, provide them to improve p-value estimation and (with
`--norm-method control`) normalization. Control files list one ID per line
(`control_sgrna.txt` = sgRNA IDs, `control_gene.txt` = gene IDs).

    # control sgRNAs
    mageck2 test -k sample.txt -t HL60.final,KBM7.final -c HL60.initial,KBM7.initial \
        -n demo_ctrlsg --norm-method control --control-sgrna control_sgrna.txt

    # or control genes
    mageck2 test -k sample.txt -t HL60.final,KBM7.final -c HL60.initial,KBM7.initial \
        -n demo_ctrlgene --norm-method control --control-gene control_gene.txt

The same `--control-sgrna` / `--control-gene` options work with `mle`. Notes:

- Use enough control guides (>100 recommended) for a reliable estimate.
- Non-targeting controls can inflate false positives in growth screens
  ([Morgens et al. 2017](https://www.nature.com/articles/ncomms15178)); the
  [MAGeCKFlute](https://www.nature.com/articles/s41596-018-0113-7) non-essential
  gene list is a good source of controls.

---

# Counting special library types

## 6. Counting screens with UMIs

*(demo folder: `demo6_countumi`)*

For screens with unique molecular identifiers (UMIs), add `--umi auto` to `count`;
mageck2 locates the UMI region automatically:

    mageck2 count -l ibar_library.txt --umi auto -n count/ibar_hela \
        --sample-label tcb_r1,tcb_r2,ref_r1,ref_r2 \
        --fastq fastq/SRR7975605_1.fastq.gz fastq/SRR7975606_1.fastq.gz \
                fastq/SRR7975595_1.fastq.gz fastq/SRR7975596_1.fastq.gz

The log reports the detected UMI window (e.g. *"UMI found in the first read.
Position (after guide): 19-25"*). Besides the usual count table, this writes a
`*.umi_count.txt` file whose rows are `sgRNA+UMI`, `sgRNA`, then per-sample counts.
If you know the UMI position, set it explicitly with `--umi-start/--umi-end` (or
`--umi-start-2/--umi-end-2` for read 2) instead of `auto`.

## 7. Counting paired-guide (dual-sgRNA) screens

*(demo folder: `demo7_count_paired_guide`)*

For vectors carrying two guides, provide the second library with `--list-seq-2`
and `--pairguide auto`:

    mageck2 count -l lib/Cpf1_lib.txt -n count/pg_test \
        --sample-label HAP1_Dual,HAP1_Dual_Torin1 \
        --pairguide auto --reverse-complement --list-seq-2 lib/Cas9_lib.txt \
        --fastq   fastq/SRR10969645_1.fastq.gz fastq/SRR10969652_1.fastq.gz \
        --fastq-2 fastq/SRR10969645_2.fastq.gz fastq/SRR10969652_2.fastq.gz

This writes a `*.pg_count.txt` file whose rows are the two concatenated sgRNA IDs
and the two concatenated gene names, followed by per-sample counts. Use
`--reverse-complement` / `--reverse-complement-2` if a guide library is stored on
the opposite strand, and `--pg-pair-only <file>` to restrict output to a defined
list of allowed guide pairs (one `sgid_1 sgid_2` pair per line).

---

# Advanced analysis

## 8. Correcting copy-number variation (CNV) effects

*(demo folders: `demo4_rra_with_cnv_correction`, `demo3_mle_with_cnv_correction`)*

Amplified regions carry more Cas9 cut sites and can appear falsely essential.
Supply a CNV matrix with `--cnv-norm` to correct for this in either `test` or
`mle`. The matrix is tab-separated with a first header that **must** be `SYMBOL`,
then one column of log2 copy-number ratios per cell line:

    SYMBOL    HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE
    A1BG      0.1105
    NAT2      0.0104

Value meaning (log2 ratio): `0` = no change, `-1` = heterozygous loss, `-2` =
homozygous loss, `>1` = amplification. Ready-made "byGene" profiles can be obtained
from [DepMap/CCLE](https://depmap.org/portal/). See the
[CNV file format](FILE_FORMATS.md#cnv-files---cnv-norm---cnv-est).

For **RRA**, name the cell line to use with `--cell-line` (it must match a CNV
column header exactly, or no correction is applied):

    mageck2 test -k sample.txt -t HL60.final,KBM7.final -c HL60.initial,KBM7.initial \
        -n demo4 --cnv-norm cnv_data.txt --cell-line HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE

For **MLE**, mageck2 matches the design-matrix condition labels to the CNV columns
automatically; or override with `--cell-line`:

    # auto-match design labels to CNV columns
    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia \
        --cnv-norm cnv_data.txt --permutation-round 2

    # or force a specific cell line
    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia_hl60 \
        --cnv-norm cnv_data.txt --permutation-round 2 \
        --cell-line HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE

If you have no measured CNV profile, `--cnv-est` can estimate one from the screen
data given a BED file of gene positions.

## 9. Complex experimental designs

The power of MLE is that the design matrix can encode arbitrary designs. Consider a
time-series drug screen: a `day0` reference plus DMSO- and estrogen (E2)-treated
samples collected at weeks 1–4. There are several ways to model it, from most
flexible to most constrained.

**Option A — one beta per sample.** Give every treated sample its own column. You
get eight independent beta scores that you can cluster afterwards. Most flexible,
but with no explicit test of a treatment effect.

**Option B — factor out shared, time, and drug effects:**

    sample      baseline  common  latevsearly  E2
    day0        1         0       0            0
    dmso-1wk    1         1       0            0
    e2-1wk      1         1       0            1
    dmso-2wk    1         1       0            0
    e2-2wk      1         1       0            1
    dmso-3wk    1         1       1            0
    e2-3wk      1         1       1            1
    dmso-4wk    1         1       1            0
    e2-4wk      1         1       1            1

- `common` — the effect shared by all treated samples; a negative beta marks genes
  essential in DMSO.
- `latevsearly` — weeks 3–4 vs. weeks 1–2; negative = more essential late.
- `E2` — E2-treated vs. DMSO; negative = more essential under estrogen.

**Option C — treat time as a linear covariate:**

    sample      baseline  time  E2
    day0        1         0     0
    dmso-1wk    1         1     0
    e2-1wk      1         1     1
    dmso-2wk    1         2     0
    e2-2wk      1         2     1
    dmso-3wk    1         3     0
    e2-3wk      1         3     1
    dmso-4wk    1         4     0
    e2-4wk      1         4     1

Here `time` assumes the log fold change scales with the week number (a guide that
halves the population per week gives log2 changes of −1, −2, −3, −4). The `E2`
column again captures the estrogen-specific difference. A gene with a positive
`time` beta but a negative `E2` beta, for instance, behaves as a tumor suppressor
under DMSO whose role reverses under estrogen.

**Paired designs.** When replicates are paired (each replicate has its own control
and treatment), you can either use RRA with `--paired`:

    mageck2 test -k count_table.txt -t treatment_rep1,treatment_rep2 -c control_rep1,control_rep2 -n paired --paired

or model it in MLE with a replicate column:

    sample           baseline  t_vs_c  rep2_vs_rep1
    control_rep1     1         0       0
    control_rep2     1         0       1
    treatment_rep1   1         1       0
    treatment_rep2   1         1       1

`t_vs_c` is the treatment-vs-control effect; `rep2_vs_rep1` absorbs the biological
difference between replicates so it does not contaminate the treatment estimate.

## 10. Mismatch-tolerant read mapping

By default `count` requires an exact guide match. To tolerate sequencing
mismatches, align with an external aligner (e.g.
[Bowtie2](https://bowtie-bio.sourceforge.net/bowtie2/)) and pass the resulting
SAM/BAM to `count` (supported since v0.5.5).

    # 1. build a FASTA from the library (id + sequence) and index it
    awk -F ',' '{print ">"$1"\n"$2}' yusa_library.csv > yusa_lib.fa
    bowtie2-build yusa_lib.fa bowtie2_ind_yusa

    # 2. align, trimming the 23-nt 5' and 8-nt 3' constant regions; --norc keeps
    #    guides from mapping to their reverse complement
    bowtie2 -x bowtie2_ind_yusa -U ERR376999.fastq.gz -5 23 -3 8 --norc \
        | samtools view -bS - > ERR376999.bam
    bowtie2 -x bowtie2_ind_yusa -U ERR376998.fastq.gz -5 23 -3 8 --norc \
        | samtools view -bS - > ERR376998.bam

    # 3. count from the BAM files instead of FASTQ
    mageck2 count -l yusa_library.csv -n escneg --sample-label "plasmid,ESC1" \
        --fastq ERR376998.bam ERR376999.bam

Trim/`--norc` settings matter: adapters must be removed before mapping, and
reverse-complement mapping disabled. Be aware that multi-mapping reads can be
counted more than once, which may distort counts.

## 11. Incorporating sgRNA efficiency

MLE can weight guides by their predicted cutting efficiency. Efficiencies can be
computed with an external tool such as
[SSC](https://sourceforge.net/projects/spacerscoringcrispr/)
([Xu et al., Genome Res 2015](https://genome.cshlp.org/content/25/8/1147)), which
outputs a table of sequence, id, gene, and an efficiency score.

Pass that table to `mle`, telling it which columns hold the sgRNA id and the score
(0-based indices):

    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia \
        --sgrna-efficiency tim.library.ssc.out \
        --sgrna-eff-name-column 1 \
        --sgrna-eff-score-column 3

Guides predicted to be inefficient are down-weighted when estimating beta scores;
see the [`mle` options](USAGE.md#mle).

---

## A note on Docker

The legacy `davidliwei/mageck` Docker image ships the original MAGeCK, not mageck2.
A mageck2 container is not yet published; install with `pip` (see
[installation](INSTALL.md)) in the meantime.

See the [FAQ](FAQ.md) for troubleshooting and results-interpretation guidance.
