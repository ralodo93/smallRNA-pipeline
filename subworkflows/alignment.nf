include { BOWTIE_ALIGN } from '../modules/bowtie_align'
include { SAMTOBAM } from '../modules/samtools'
include { SORTBAM } from '../modules/samtools'

workflow ALIGNMENT {
    take:
    reads
    index_files
    index_name


    main:
    BOWTIE_ALIGN(reads, index_files, index_name)
    SAMTOBAM(BOWTIE_ALIGN.out.sam)
    SORTBAM(SAMTOBAM.out.bam)

    emit:
    bam = SORTBAM.out.bam
}