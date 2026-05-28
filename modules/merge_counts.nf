process MERGE_COUNTS {
    publishDir { "${params.outdir}/counts" }, mode: 'copy'

    input:
    path count_files

    output:
    path "merged_counts.txt", emit: merged

    script:
    """
    merge_counts.py ${count_files}
    """
}