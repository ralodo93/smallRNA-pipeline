process TRIM_READS {
    tag "${sample}"
    publishDir { "${params.outdir}/trimmed" }, mode: 'copy'

    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path("${sample}_trimmed.fastq.gz"), emit: trimmed
    path "${sample}_cutadapt.log",                         emit: log    // ← añadido

    script:
    """
    cutadapt -j ${params.threads} -m 10 -M 50 \
        -o ${sample}_trimmed.fastq.gz \
        ${reads} \
        > ${sample}_cutadapt.log
    """
}