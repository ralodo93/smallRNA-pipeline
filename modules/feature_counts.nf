process FEATURE_COUNTS {
    tag "${sample}"
    
    publishDir { "${params.outdir}/counts" }, mode: 'copy'

    input:
    tuple val(sample), path(bam)
    path annotation

    output:
    tuple val(sample), path("${sample}.txt"), emit: counts

    script:
    """
    featureCounts -T ${params.threads} -t miRNA -g Name -s 1 -O -a ${annotation} -o ${sample}.txt ${bam}
    """
}