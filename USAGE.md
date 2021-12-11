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

The relative start position of UMI from guides, if UMI
                        is found on the first pair. For example, for a read
                        NNNNAATACGNNNCGACNNNN with guide AATACG and UMI CGAC,
                        set --umi-start to 4 and --umi-end to 8.
                        
*  --pg-end PG_END       

The relative end position of UMI from guides, if UMI
                        is found on the first pair.
                        
*  --pg-start-2 PG_START_2

The relative start position of UMI (from the first
                        nucleotide of the read), if UMI is found on the second
                        pair. For example, for a read NNNNCGAC with UMI CGAC,
                        set --umi-start-2 to 4 and --umi-end-2 to 8.
                        
*  --pg-end-2 PG_END_2   

The relative end position of UMI (from the first
                        nucleotide of the read), if UMI is found on the second
                        pair.
                        
*  --pg-min-read PG_MIN_READ

Only report paired-guides whose total reads in all
                        samples no less than this number. Setting to higher
                        numbers to avoid reporting a large number of records
                        with very few reads. Default 2.
                        
*  --pg-pair-only PG_PAIR_ONLY

Only report paired-guides whose combination is listed
                        in the file designated by --pg-pair-only. Each line in
                        this file should has the format "sgid_1 sgid_2", where
                        sgid_1 and sgid_2 are sgRNA IDs from --list-seq and
                        --list-seq-2, respectively.
