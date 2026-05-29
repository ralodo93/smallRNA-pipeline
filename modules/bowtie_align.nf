process BOWTIE_ALIGN {
    tag "${sample}"

    input:
    tuple val(sample), path(reads)
    path  index_files
    val   index_name

    output:
    tuple val(sample), path("${sample}.sam"), emit: sam
    path "${sample}_bowtie.log",              emit: log  // ← captura stderr

    script:
    """
    bowtie -n 0 -l 18 --best --nomaqround -e 70 -k 1 -S -p ${params.threads} -x ${index_name} ${reads} > ${sample}.sam 2> ${sample}_bowtie.log
    """
}