process BOWTIE_BUILD {
    publishDir "${params.genomedir}/${params.index_name}", mode: 'copy'

    input:
    path fasta

    output:
    path "${params.index_name}*.ebwt", emit: ebwt_files
    val  "${params.index_name}",       emit: prefix

    script:
    """
    bowtie-build --threads ${params.threads} ${fasta} ${params.index_name}
    """
}