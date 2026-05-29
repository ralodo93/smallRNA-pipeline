process FEATURE_COUNTS {
    tag "${sample}"
    
    publishDir { "${params.outdir}/counts" }, mode: 'copy'

    input:
    tuple val(sample), path(bam)
    path annotation

    output:
    tuple val(sample), path("${sample}.txt"), emit: counts
    path "${sample}.txt.summary", emit: summary

    script:
    """
    featureCounts -T ${params.threads} -t miRNA -g Name -s 1 -O -a ${annotation} -o ${sample}.txt ${bam}
    """
}