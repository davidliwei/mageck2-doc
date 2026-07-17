# mageck2 usage

## Subcommands


* count: only collect sgRNA read counts from read mapping files (sam format).
* test: given a table of read counts, perform the sgRNA and gene ranking using RRA.
* mle: perform maximum-likelihood estimation of gene essentiality scores.
* pathway: given a ranked gene list, test whether one pathway is enriched.


## count


### usage:

    mageck2 count [-h] [-l LIST_SEQ]
                     (--fastq FASTQ [FASTQ ...] | -k COUNT_TABLE)
                     [--norm-method {none,median,total,control}]
                     [--control-sgrna CONTROL_SGRNA | --control-gene CONTROL_GENE]
                     [--sample-label SAMPLE_LABEL] [-n OUTPUT_PREFIX]
                     [--unmapped-to-file] [--keep-tmp] [--test-run]
                     [--fastq-2 FASTQ_2 [FASTQ_2 ...]]
                     [--count-pair COUNT_PAIR] [--trim-5 TRIM_5]
                     [--sgrna-len SGRNA_LEN] [--count-n]
                     [--reverse-complement] [--pdf-report]
                     [--day0-label DAY0_LABEL] [--gmt-file GMT_FILE]
                     [--umi {none,firstpair,secondpair,auto}]
                     [--umi-start UMI_START] [--umi-end UMI_END]
                     [--umi-start-2 UMI_START_2] [--umi-end-2 UMI_END_2]
                     [--pairguide {none,firstpair,secondpair,auto}]
                     [--list-seq-2 LIST_SEQ_2] [--reverse-complement-2]
                     [--pg-start PG_START] [--pg-end PG_END]
                     [--pg-start-2 PG_START_2] [--pg-end-2 PG_END_2]
                     [--pg-min-read PG_MIN_READ] [--pg-pair-only PG_PAIR_ONLY]

### options:

*  -h, --help            

show this help message and exit

### Required arguments:

*  -l LIST_SEQ, --list-seq LIST_SEQ

A file containing the list of sgRNA names, their sequences and associated genes. Support file format: csv and txt. Provide an empty file for collecting all possible sgRNA counts.

*  --fastq FASTQ [FASTQ ...]

Sample fastq files (or fastq.gz files, or SAM/BAM
                        files after v0.5.5), separated by space; use comma (,)
                        to indicate technical replicates of the same sample.
                        For example, "--fastq
                        sample1_replicate1.fastq,sample1_replicate2.fastq
                        sample2_replicate1.fastq,sample2_replicate2.fastq"
                        indicates two samples with 2 technical replicates for
                        each sample.
                        
*  -k COUNT_TABLE, --count-table COUNT_TABLE

The read count table file. Only 1 file is accepted.


### Optional arguments for normalization:

*  --norm-method {none,median,total,control}

Method for normalization, including "none" (no
                        normalization), "median" (median normalization,
                        default), "total" (normalization by total read
                        counts), "control" (normalization by control sgRNAs
                        specified by the --control-sgrna option).

*   --control-sgrna CONTROL_SGRNA

A list of control sgRNAs for normalization and for
                        generating the null distribution of RRA.



* --control-gene CONTROL_GENE

A list of genes whose sgRNAs are used as control
                        sgRNAs for normalization and for generating the null
                        distribution of RRA.

### Optional arguments for input and output:

*  --sample-label SAMPLE_LABEL
 
Sample labels, separated by comma (,). Must be equal
                        to the number of samples provided (in --fastq option).
                        Default "sample1,sample2,...".

*  -n OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX

The prefix of the output file(s). Default sample1.

*  --unmapped-to-file    

Save unmapped reads to file, with sgRNA lengths
                        specified by --sgrna-len option.

*  --keep-tmp            
Keep intermediate files.

*  --test-run            

Test running. If this option is on, MAGeCK will only
                        process the first 1M records for each file.

### Optional arguments for processing fastq files:

*  --fastq-2 FASTQ_2 [FASTQ_2 ...]

Paired sample fastq files (or fastq.gz files), the
                        order of which should be consistent with that in fastq
                        option.
                        
*  --count-pair COUNT_PAIR
                        
Report all valid alignments per read or pair (default:
                        False).
*  --trim-5 TRIM_5       

Length of trimming the 5' of the reads. Users can
                        specify multiple trimming lengths, separated by comma
                        (,); for example, "7,8". Use "AUTO" to allow MAGeCK to
                        automatically determine the trimming length. Default
                        AUTO.
*  --sgrna-len SGRNA_LEN

Length of the sgRNA. Default 20. ATTENTION: after
                        v0.5.3, the program will automatically determine the
                        sgRNA length from library file; so only use this if
                        you turn on the --unmapped-to-file option.
*  --count-n             

Count sgRNAs with Ns. By default, sgRNAs containing N
                        will be discarded.
*  --reverse-complement 

Reverse complement the sequences in library for read
                        mapping. Note: for performance considerations, only
                        the guide sequences are reverse complemented, not the
                        read.

## Optional arguments for quality controls:


*  --day0-label DAY0_LABEL
                        
Turn on the negative selection QC and specify the
                        label for control sample (usually day 0 or plasmid).
                        For every other sample label, the negative selection
                        QC will compare it with day0 sample, and estimate the
                        degree of negative selections in essential genes.
*  --gmt-file GMT_FILE   

The pathway file used for QC, in GMT format. By
                        default it will use the GMT file provided by MAGeCK.
                        

### Optional arguments for searching for UMIs:

*  --umi {none,firstpair,secondpair,auto}

Search UMIs, located within the first pair or the
                        second pair of the read, or automatically search for
                        possible UMIs. If you are aware of the location of the
                        UMI, specify the values of --umi-start/--umi-end (if
                        --umi firstpair), or --umi-start-2/--umi-end-2 (if
                        --umi secondpair). The program will automatically
                        search for UMI locations if --umi auto.
                        
*  --umi-start UMI_START

The relative start position of UMI from guides, if UMI
                        is found on the first pair. For example, for a read
                        NNNNAATACGNNNCGACNNNN with guide AATACG and UMI CGAC,
                        set --umi-start to 4 and --umi-end to 8.
                        
*  --umi-end UMI_END     

The relative end position of UMI from guides, if UMI
                        is found on the first pair.
                        
*  --umi-start-2 UMI_START_2

The relative start position of UMI (from the first
                        nucleotide of the read), if UMI is found on the second
                        pair. For example, for a read NNNNCGAC with UMI CGAC,
                        set --umi-start-2 to 4 and --umi-end-2 to 8.
                        
*  --umi-end-2 UMI_END_2

The relative end position of UMI (from the first
                        nucleotide of the read), if UMI is found on the second
                        pair.


### Optional arguments for counting paired-guide screens:

*  --pairguide {none,firstpair,secondpair,auto}

Search for second gRNA, located within the first pair
                        or the second pair of the read, or automatically
                        search for possible guides. If you are aware of the
                        location of the guide, specify the values of --pg-
                        start/--pg-end (if --pairguide firstpair), or --pg-
                        start-2/--pg-end-2 (if --pairguide secondpair). The
                        program will automatically search for locations if
                        --pairguide auto.
                        
*  --list-seq-2 LIST_SEQ_2

A library file for the second sgRNA, containing the
                        list of sgRNA names, their sequences and associated
                        genes. Support file format: csv and txt.
                        
*  --reverse-complement-2

Reverse complement the sequences in the second pair
                        guide library for read mapping. Note: for performance
                        considerations, only the guide sequences are reverse
                        complemented, not the read.
                        
*  --pg-start PG_START   

The relative start position of the second guide,
                        measured from the end of the first guide, when the
                        second guide is on the first read (--pairguide
                        firstpair). For a second guide immediately following
                        the first guide, set --pg-start to 0.
                        
*  --pg-end PG_END       

The relative end position of the second guide, measured
                        from the end of the first guide, when the second guide
                        is on the first read (--pairguide firstpair).
                        
*  --pg-start-2 PG_START_2

The relative start position of the second guide,
                        measured from the first nucleotide of the second read,
                        when the second guide is on the second read
                        (--pairguide secondpair). For example, for a 20bp
                        second guide at the very start of read 2, set
                        --pg-start-2 to 0 and --pg-end-2 to 20.
                        
*  --pg-end-2 PG_END_2   

The relative end position of the second guide, measured
                        from the first nucleotide of the second read, when the
                        second guide is on the second read (--pairguide
                        secondpair).
                        
*  --pg-min-read PG_MIN_READ

Only report paired-guides whose total reads in all
                        samples no less than this number. Setting to higher
                        numbers to avoid reporting a large number of records
                        with very few reads. Default 3.
                        
*  --pg-pair-only PG_PAIR_ONLY

Only report paired-guides whose combination is listed
                        in the file designated by --pg-pair-only. Each line in
                        this file should has the format "sgid_1 sgid_2", where
                        sgid_1 and sgid_2 are sgRNA IDs from --list-seq and
                        --list-seq-2, respectively.


## test

Given a count table (from the `count` command or your own), perform sgRNA- and
gene-level ranking using the Robust Rank Aggregation (RRA) algorithm, comparing
treatment vs. control samples. Outputs `[prefix].gene_summary.txt` and
`[prefix].sgrna_summary.txt` (see [file formats](FILE_FORMATS.md)).

### usage:

    mageck2 test [-h] -k COUNT_TABLE (-t TREATMENT_ID | --day0-label DAY0_LABEL)
                    [-c CONTROL_ID] [--paired]
                    [--norm-method {none,median,total,control}]
                    [--gene-test-fdr-threshold GENE_TEST_FDR_THRESHOLD]
                    [--adjust-method {fdr,holm,pounds}]
                    [--variance-estimation-samples VARIANCE_ESTIMATION_SAMPLES]
                    [--sort-criteria {neg,pos}]
                    [--remove-zero {none,control,treatment,both,any}]
                    [--remove-zero-threshold REMOVE_ZERO_THRESHOLD]
                    [--pdf-report]
                    [--gene-lfc-method {median,alphamedian,mean,alphamean,secondbest}]
                    [-n OUTPUT_PREFIX]
                    [--control-sgrna CONTROL_SGRNA | --control-gene CONTROL_GENE]
                    [--normcounts-to-file] [--skip-gene SKIP_GENE] [--keep-tmp]
                    [--additional-rra-parameters ADDITIONAL_RRA_PARAMETERS]
                    [--cnv-norm CNV_NORM] [--cell-line CELL_LINE] [--cnv-est CNV_EST]

### Required arguments:

*  -k COUNT_TABLE, --count-table COUNT_TABLE

A tab-separated count table. Each line should include the sgRNA name (1st column), gene name (2nd column) and read counts in each sample.

One of the following (mutually exclusive) is required to define the treatment:

*  -t TREATMENT_ID, --treatment-id TREATMENT_ID

Sample label(s) or index(es) (0 as the first sample) in the count table used as treatment experiments, separated by comma (,). Labels must match the first line of the count table (e.g. "HL60.final,KBM7.final"); indexes such as "0,2" select the 1st and 3rd samples.

*  --day0-label DAY0_LABEL

Specify the label for the control sample (usually day 0 or plasmid). Every other sample is treated as a treatment condition and compared with the control.

### Optional general arguments:

*  -c CONTROL_ID, --control-id CONTROL_ID

Control sample label(s) or index(es), separated by comma (,). Default: all samples not listed as treatment.

*  --paired

Paired-sample comparison. The number of samples in `-t` and `-c` must match and be in the same order (e.g. "-t treatment_r1,treatment_r2 -c control_r1,control_r2").

*  --norm-method {none,median,total,control}

Normalization method: "none", "median" (default), "total" (by total read counts), or "control" (by control sgRNAs from `--control-sgrna`).

*  --gene-test-fdr-threshold GENE_TEST_FDR_THRESHOLD

p-value threshold determining the alpha value of RRA in the gene test (RRA `-p`). Default 0.25.

*  --adjust-method {fdr,holm,pounds}

sgRNA-level p-value adjustment: false discovery rate (fdr, default), Holm's method (holm), or Pounds's method (pounds).

*  --variance-estimation-samples VARIANCE_ESTIMATION_SAMPLES

Sample label(s)/index(es) for estimating variances, separated by comma (,).

*  --sort-criteria {neg,pos}

Sort by negative selection (neg, default) or positive selection (pos).

*  --remove-zero {none,control,treatment,both,any}

Remove sgRNAs whose mean value is zero in the given samples. Default: both.

*  --remove-zero-threshold REMOVE_ZERO_THRESHOLD

Normalized-count threshold below which an sgRNA is considered zero for `--remove-zero`. Default 0.

*  --pdf-report

Generate a PDF report of the analysis.

*  --gene-lfc-method {median,alphamedian,mean,alphamean,secondbest}

Method to compute gene log2 fold change from sgRNA LFCs: median/mean of all sgRNAs, median/mean of sgRNAs ranked ahead of the RRA alpha cutoff (alphamedian/alphamean), or the second-strongest sgRNA (secondbest). Default median.

### Optional arguments for input and output:

*  -n OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX

Prefix of the output file(s). Default sample1.

*  --control-sgrna CONTROL_SGRNA

A list of control sgRNAs for normalization and for generating the RRA null distribution.

*  --control-gene CONTROL_GENE

A list of genes whose sgRNAs are used as control sgRNAs (mutually exclusive with `--control-sgrna`).

*  --normcounts-to-file

Write normalized read counts to `[output-prefix].normalized.txt`.

*  --skip-gene SKIP_GENE

Skip a gene in the report (repeatable). By default "NA"/"na" are skipped.

*  --keep-tmp

Keep intermediate files.

*  --additional-rra-parameters ADDITIONAL_RRA_PARAMETERS

Extra arguments appended to the RRA command line.

### Optional arguments for CNV correction:

*  --cnv-norm CNV_NORM

A matrix of copy-number-variation data across cell lines, used to correct CNV-biased sgRNA scores before gene ranking.

*  --cell-line CELL_LINE

The cell line used for CNV normalization; must match a column name in `--cnv-norm`.

*  --cnv-est CNV_EST

Estimate CNV profiles from the screening data. Requires a BED file of gene positions.


## mle

Perform maximum-likelihood estimation (MLE) of gene essentiality (beta scores)
under a user-supplied experimental design matrix. Supports complex designs
(time-series, multiple conditions, drug treatments). Outputs
`[prefix].gene_summary.txt` (beta scores) and `[prefix].sgrna_summary.txt`
(see [file formats](FILE_FORMATS.md)).

### usage:

    mageck2 mle [-h] -k COUNT_TABLE (-d DESIGN_MATRIX | --day0-label DAY0_LABEL)
                   [-n OUTPUT_PREFIX] [-i INCLUDE_SAMPLES] [-b BETA_LABELS]
                   [--control-sgrna CONTROL_SGRNA | --control-gene CONTROL_GENE]
                   [--cnv-norm CNV_NORM] [--cell-line CELL_LINE] [--cnv-est CNV_EST]
                   [--debug] [--debug-gene DEBUG_GENE]
                   [--norm-method {none,median,total,control}]
                   [--genes-varmodeling GENES_VARMODELING]
                   [--permutation-round PERMUTATION_ROUND]
                   [--no-permutation-by-group]
                   [--max-sgrnapergene-permutation MAX_SGRNAPERGENE_PERMUTATION]
                   [--remove-outliers] [--threads THREADS]
                   [--adjust-method {fdr,holm,pounds}]
                   [--sgrna-efficiency SGRNA_EFFICIENCY]
                   [--sgrna-eff-name-column SGRNA_EFF_NAME_COLUMN]
                   [--sgrna-eff-score-column SGRNA_EFF_SCORE_COLUMN]
                   [--update-efficiency] [--bayes] [-p] [-w PPI_WEIGHTING]
                   [-e NEGATIVE_CONTROL]

### Required arguments:

*  -k COUNT_TABLE, --count-table COUNT_TABLE

A tab-separated count table. Each line should include the sgRNA name (1st column), target gene (2nd column) and read counts in each sample.

One of the following (mutually exclusive) is required:

*  -d DESIGN_MATRIX, --design-matrix DESIGN_MATRIX

A design matrix, given as a file name or a quoted string (e.g. "1,1;1,0"). Rows must match the order of samples in the count table (or the order given by `--include-samples`). See [file formats](FILE_FORMATS.md#design-matrix) for the file layout.

*  --day0-label DAY0_LABEL

Specify the label for the control sample (usually day 0 or plasmid); a corresponding design matrix is generated automatically, treating every other sample as a condition.

### Optional arguments for input and output:

*  -n OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX

Prefix of the output file(s). Default sample1.

*  -i INCLUDE_SAMPLES, --include-samples INCLUDE_SAMPLES

Sample labels to include when the design matrix is given as a string (not a file). Comma-separated; must match labels in the count table.

*  -b BETA_LABELS, --beta-labels BETA_LABELS

Labels of the beta variables when the design matrix is given as a string. Comma-separated; the count must equal the number of design-matrix columns (including baseline). Default "beta_0,beta_1,...".

*  --control-sgrna CONTROL_SGRNA / --control-gene CONTROL_GENE

A list of control sgRNAs, or genes whose sgRNAs are used as controls, for normalization and null-distribution generation (mutually exclusive).

### Optional arguments for CNV correction:

*  --cnv-norm CNV_NORM

A matrix of CNV data across cell lines, used to correct CNV-biased sgRNA scores before gene ranking.

*  --cell-line CELL_LINE

The cell line used for CNV normalization; must match a column name in `--cnv-norm`. Overrides the default of inferring cell-line names from the design-matrix columns.

*  --cnv-est CNV_EST

Estimate CNV profiles from the screening data. Requires a BED file of gene positions.

### Optional arguments for the MLE module:

*  --debug / --debug-gene DEBUG_GENE

Output detailed running information, or run only a single gene by ID.

*  --norm-method {none,median,total,control}

Normalization method (see `test`). Default median.

*  --genes-varmodeling GENES_VARMODELING

Number of genes used for mean-variance modeling. Default 0.

*  --permutation-round PERMUTATION_ROUND

Rounds of permutation; total permutations = (#genes) × rounds. Suggested 10 (slower). Default 2.

*  --no-permutation-by-group

Permute all genes together instead of separately by sgRNA count. Faster, but p-values are accurate only when sgRNA-per-gene counts are similar.

*  --max-sgrnapergene-permutation MAX_SGRNAPERGENE_PERMUTATION

Skip beta-score / p-value computation for genes targeted by more than this many sgRNAs. Default 40.

*  --remove-outliers

Attempt to remove outliers (slower).

*  --threads THREADS

Number of threads. Default 1.

*  --adjust-method {fdr,holm,pounds}

sgRNA-level p-value adjustment method. Default fdr.

### Optional arguments for the EM iteration:

*  --sgrna-efficiency SGRNA_EFFICIENCY

A file of sgRNA efficiency predictions, used as the initial guess of each sgRNA's efficiency. At least two columns: sgRNA ID and efficiency.

*  --sgrna-eff-name-column SGRNA_EFF_NAME_COLUMN

Column (0-based) of the sgRNA ID in the efficiency file. Default 0.

*  --sgrna-eff-score-column SGRNA_EFF_SCORE_COLUMN

Column (0-based) of the efficiency score in the efficiency file. Default 1.

*  --update-efficiency

Iteratively update sgRNA efficiency during EM iteration.

### Optional arguments for Bayes estimation (experimental):

*  --bayes

Use the experimental Bayes module to estimate gene essentiality.

*  -p, --PPI-prior

Incorporate protein-protein interaction (PPI) information as a prior.

*  -w PPI_WEIGHTING, --PPI-weighting PPI_WEIGHTING

Weighting used to compute the PPI prior. If omitted, it is determined iteratively.

*  -e NEGATIVE_CONTROL, --negative-control NEGATIVE_CONTROL

Gene name of negative controls; the corresponding sgRNAs are viewed independently.


## pathway

Given a gene ranking from the `test` command, test whether gene sets / pathways
(in GMT format) are enriched, using GSEA or RRA. Enrichment is evaluated in both
the negative- and positive-selection directions unless `--single-ranking` is set.

### usage:

    mageck2 pathway [-h] --gene-ranking GENE_RANKING --gmt-file GMT_FILE
                       [-n OUTPUT_PREFIX] [--method {gsea,rra}] [--single-ranking]
                       [--sort-criteria {neg,pos}] [--keep-tmp]
                       [--ranking-column RANKING_COLUMN]
                       [--ranking-column-2 RANKING_COLUMN_2]
                       [--pathway-alpha PATHWAY_ALPHA] [--permutation PERMUTATION]

### Required arguments:

*  --gene-ranking GENE_RANKING

The `gene_summary` file (with both positive and negative selection tests) produced by the `test` command.

*  --gmt-file GMT_FILE

The pathway / gene-set file in GMT format.

### Optional arguments:

*  -n OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX

Prefix of the output file(s). Default sample1.

*  --method {gsea,rra}

Enrichment method: GSEA (default) or RRA.

*  --single-ranking

Treat the input as a single-direction ranking (positive or negative); only one enrichment comparison is performed.

*  --sort-criteria {neg,pos}

Sort by negative (default) or positive selection.

*  --ranking-column RANKING_COLUMN

Column (integer index or label) in the gene summary used for ranking. Default "2" (the negative-selection RRA score).

*  --ranking-column-2 RANKING_COLUMN_2

Column for the opposite (positive-selection) direction. Default "8". Disabled with `--single-ranking`.

*  --pathway-alpha PATHWAY_ALPHA

Alpha value for RRA pathway enrichment. Default 0.25.

*  --permutation PERMUTATION

Number of permutations for GSEA. Default 1000.

*  --keep-tmp

Keep intermediate files.


## plot

Generate per-gene graphics (e.g. sgRNA read-count and rank plots) for selected
genes from a count table and a `test` gene summary.

### usage:

    mageck2 plot [-h] -k COUNT_TABLE -g GENE_SUMMARY [--genes GENES] [-s SAMPLES]
                    [-n OUTPUT_PREFIX] [--norm-method {none,median,total,control}]
                    [--control-sgrna CONTROL_SGRNA | --control-gene CONTROL_GENE]
                    [--keep-tmp]

### Required arguments:

*  -k COUNT_TABLE, --count-table COUNT_TABLE

A tab-separated count table (sgRNA, gene, per-sample read counts).

*  -g GENE_SUMMARY, --gene-summary GENE_SUMMARY

The `gene_summary` file generated by the `test` command.

### Optional arguments:

*  --genes GENES

Comma-separated list of genes to plot. Default: none.

*  -s SAMPLES, --samples SAMPLES

Comma-separated list of samples to plot. Default: all samples in the count table.

*  -n OUTPUT_PREFIX, --output-prefix OUTPUT_PREFIX

Prefix of the output file(s). Default sample1.

*  --norm-method {none,median,total,control}

Normalization method (see `test`). Default median.

*  --control-sgrna CONTROL_SGRNA / --control-gene CONTROL_GENE

Control sgRNAs, or genes whose sgRNAs are used as controls, for normalization (mutually exclusive).

*  --keep-tmp

Keep intermediate files.
