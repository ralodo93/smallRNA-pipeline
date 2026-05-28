process DOWNLOAD_FASTA {
    publishDir "${params.genomedir}", mode: 'copy'

    output:
    path "${params.fasta_url.split('/').last()}", emit: fasta_gz  // emit the exact path

    script:
    """
    wget -q ${params.fasta_url}
    """
}