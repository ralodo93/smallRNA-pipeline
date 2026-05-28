process DOWNLOAD_FASTA {
    publishDir "${params.genomedir}", mode: 'copy'

    input:
    val url

    output:
    path "${url.split('/').last()}", emit: fasta_gz // ← ahora se evalúa en ejecución

    script:
    """
    wget -q ${url}
    """
}