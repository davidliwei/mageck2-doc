# Tutorials

These tutorials walk through common mageck2 workflows. Every example corresponds
to a folder in the [mageck2-demo](https://github.com/davidliwei/mageck2-demo)
repository that contains the input data and a `run.sh` script — clone that repo
and run the commands below from inside the matching folder.

**Prerequisite:** install mageck2 first (see [installation](INSTALL.md)). For the
input/output file layouts referenced here, see [file formats](FILE_FORMATS.md);
for the full option reference, see [usage](USAGE.md).

---

## 1. RRA analysis from a read count table

*(demo folder: `demo1_rra_from_count_table`)*

The simplest workflow: given a count table, compare treatment vs. control samples
and rank sgRNAs and genes with RRA. `sample.txt` has a header line
(`sgRNA  Gene  HL60.initial  KBM7.initial  HL60.final  KBM7.final`) and one row per
sgRNA.

    mageck2 test -k sample.txt -t HL60.final,KBM7.final -c HL60.initial,KBM7.initial -n demo

Samples may also be given by index (0-based), so the following is equivalent:

    mageck2 test -k sample.txt -t 2,3 -c 0,1 -n demo

This produces `demo.gene_summary.txt`, `demo.sgrna_summary.txt`, and `demo.log`.

## 2. Starting from raw FASTQ files

*(demo folder: `demo2_run_mageck_from_fastq`)*

If you start from sequencing reads, first build a count table with `count`
(supplying an sgRNA library file), then run `test`:

    # 1. count reads against the library
    mageck2 count -l library.txt -n demo --sample-label L1,CTRL --fastq test1.fastq test2.fastq

    # 2. statistical test on the resulting count table
    mageck2 test -k demo.count.txt -t L1 -c CTRL -n demo

`count` also writes a `demo.countsummary.txt` QC file summarizing mapping rate,
zero-count sgRNAs, and the Gini index per sample.

> The old all-in-one `run` command has been discontinued; run `count` then `test`.

## 3. Multi-condition analysis with MAGeCK MLE

*(demo folder: `demo3_mle_with_cnv_correction`)*

The MLE module estimates gene **beta scores** (selection effects) across arbitrary
experimental designs, described by a design matrix. `designmat.txt` is
tab-separated, with a `Samples` column matching the count table, a required
`baseline` column of 1s, and one column per condition:

    Samples         baseline    HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE    KBM7
    HL60.initial    1           0                                          0
    KBM7.initial    1           0                                          0
    HL60.final      1           1                                          0
    KBM7.final      1           0                                          1

Run MLE with:

    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia --permutation-round 2

This produces `beta_leukemia.gene_summary.txt` (one beta/z/p-value/FDR block per
condition) and `beta_leukemia.sgrna_summary.txt`.

## 4. Correcting copy-number variation (CNV) effects

*(demo folders: `demo4_rra_with_cnv_correction`, `demo3_mle_with_cnv_correction`)*

Amplified regions can produce false positives in essentiality screens. Supply a
CNV matrix with `--cnv-norm` to correct for this. The matrix is tab-separated with
a `SYMBOL` gene column and one column of (log2) copy-number values per cell line:

    SYMBOL    HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE
    A1BG      0.1105
    NAT2      0.0104

For **RRA**, name the cell line to use with `--cell-line`:

    mageck2 test -k sample.txt -t HL60.final,KBM7.final -c HL60.initial,KBM7.initial \
        -n demo4 --cnv-norm cnv_data.txt --cell-line HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE

For **MLE**, mageck2 matches the design-matrix condition labels to the CNV columns
automatically; or override with `--cell-line`:

    # auto-match design labels to CNV columns
    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia --cnv-norm cnv_data.txt --permutation-round 2

    # or force a specific cell line
    mageck2 mle -k leukemia.new.csv -d designmat.txt -n beta_leukemia_hl60 --cnv-norm cnv_data.txt \
        --permutation-round 2 --cell-line HL60_HAEMATOPOIETIC_AND_LYMPHOID_TISSUE

If you do not have a measured CNV profile, `--cnv-est` can estimate one from the
screen data given a BED file of gene positions.

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

## 6. Counting screens with UMIs

*(demo folder: `demo6_countumi`)*

For screens with unique molecular identifiers (UMIs), add `--umi auto` to `count`;
mageck2 locates the UMI region automatically:

    mageck2 count -l ibar_library.txt --umi auto -n count/ibar_hela \
        --sample-label tcb_r1,tcb_r2,ref_r1,ref_r2 \
        --fastq fastq/SRR7975605_1.fastq.gz fastq/SRR7975606_1.fastq.gz \
                fastq/SRR7975595_1.fastq.gz fastq/SRR7975596_1.fastq.gz

Besides the usual count table, this writes a `*.umi_count.txt` file whose rows are
`sgRNA+UMI`, `sgRNA`, then per-sample counts. If you know the UMI position, set it
explicitly with `--umi-start/--umi-end` (or `--umi-start-2/--umi-end-2` for read 2)
instead of `auto`.

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
list of allowed guide pairs.

---

## Advanced notes

- **Mismatch-tolerant mapping.** mageck2 `count` accepts SAM/BAM files in place of
  FASTQ, so you can map reads with an external aligner (e.g. Bowtie2) to allow
  mismatches and pass the alignments to `count`.
- **sgRNA efficiency in MLE.** Supply predicted per-sgRNA efficiencies to `mle`
  with `--sgrna-efficiency` (see [usage](USAGE.md#mle)) to weight guides by their
  expected activity.

See the [FAQ](README.md#faq) for troubleshooting and interpretation guidance.
