include { DOWNLOAD_FASTA } from '../modules/download_fasta'
include { GUNZIP_FASTA } from '../modules/gunzip_fasta'
include { BOWTIE_BUILD } from '../modules/bowtie_build'

workflow PREPARE_GENOME {

    main:
    DOWNLOAD_FASTA()
    GUNZIP_FASTA(DOWNLOAD_FASTA.out.fasta_gz)
    BOWTIE_BUILD(GUNZIP_FASTA.out.fasta)

    index_ch = BOWTIE_BUILD.out.ebwt_files
                   .collect()                              // agrupa todos los .ebwt en una lista
                   .combine(BOWTIE_BUILD.out.prefix)      // los une con el prefijo
    
    emit:
    ebwt_files = BOWTIE_BUILD.out.ebwt_files.collect().first()  // ← value channel
    prefix     = BOWTIE_BUILD.out.prefix 
}