process FASTQC {
    tag "${sample}"
    publishDir { "${params.outdir}/${outdir_suffix}" }, mode: 'copy'

    input:
    tuple val(sample), path(reads)
    val outdir_suffix

    output:
    tuple val(sample), path("*_fastqc.zip"),  emit: zip
    tuple val(sample), path("*_fastqc.html"), emit: html

    script:
    """
    fastqc -t ${params.threads} ${reads}
    """
}