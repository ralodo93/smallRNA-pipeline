include { FASTQC as FASTQC_RAW } from '../modules/fastqc'  // ← alias
include { FASTQC as FASTQC_TRIMMED } from '../modules/fastqc'  // ← alias
include { FILTER_READS } from '../modules/filter_reads'
include { TRIM_READS } from '../modules/trim_reads'

workflow PREPROCESSING {
    take:
    reads_ch

    main:
    // 1. FASTQC on raw reads
    FASTQC_RAW(reads_ch, "fastqc_raw")
    // 2. Filter reads
    FILTER_READS(reads_ch)
    // 3. Trim filtered reads
    TRIM_READS(FILTER_READS.out.filtered)
    // 4. FASTQC on trimmed reads
    FASTQC_TRIMMED(TRIM_READS.out.trimmed, "fastqc_trimmed")

    emit:
    trimmed = TRIM_READS.out.trimmed
}