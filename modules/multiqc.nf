process MULTIQC {
    publishDir "${params.outdir}/multiqc", mode: 'copy'

    input:
    path files  // ← recibe todos los ficheros juntos

    output:
    path "multiqc_report.html", emit: report
    path "multiqc_data/",       emit: data

    script:
    """
    multiqc .
    """
}