process SAMTOBAM {
    tag "${sample}"

    input:
    tuple val(sample), path(sam)

    output:
    tuple val(sample), path("${sample}_tmp.bam"), emit: bam

    script:
    """
    samtools view --threads ${params.threads} -bS ${sam} -o ${sample}_tmp.bam
    """
}

process SORTBAM {
    tag "${sample}"

    publishDir { "${params.outdir}/aligned" }, mode: 'copy'

    input:
    tuple val(sample), path(bam)

    output:
    tuple val(sample), path("${sample}.bam"), emit: bam

    script:
    """
    samtools sort --threads ${params.threads} -o ${sample}.bam ${bam}
    """
}