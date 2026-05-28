process FILTER_READS {
    tag "${sample}"
    publishDir { "${params.outdir}/filtered" }, mode: 'copy'

    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path("${sample}_filtered.fastq.gz"), emit: filtered

    script:
    """
    filter_reads.py -i ${reads} -o ${sample}_filtered.fastq.gz --gap 3
    """
}