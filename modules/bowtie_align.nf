process BOWTIE_ALIGN {
    tag "${sample}"

    input:
    tuple val(sample), path(reads)          // ← tupla de reads
    path index_files
    val index_name

    output:
    tuple val(sample), path("${sample}.sam"), emit: sam

    script:
    """
    bowtie -p ${params.threads} -n 0 -l 18 --best --nomaqround -e 70 -k 1 -S -x ${index_name} ${reads} > ${sample}.sam
    """
}