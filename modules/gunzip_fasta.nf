process GUNZIP_FASTA {

    input:
    path fasta_gz

    output:
    path "${fasta_gz.baseName}", emit: fasta

    script:
    """
    gunzip -c ${fasta_gz} > ${fasta_gz.baseName}
    """
}