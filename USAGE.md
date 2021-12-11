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
