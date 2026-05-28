process DOWNLOAD_GFF {
    publishDir "${params.genomedir}", mode: 'copy'

    output:
    path "${params.annotation_url.split('/').last()}", emit: gff  // emit the exact path

    script:
    """
    wget -q ${params.annotation_url}
    """
}