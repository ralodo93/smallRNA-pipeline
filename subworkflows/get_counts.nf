include { DOWNLOAD_GFF } from '../modules/download_gff'
include { FEATURE_COUNTS } from '../modules/feature_counts'
include { MERGE_COUNTS } from '../modules/merge_counts'

workflow GET_COUNTS {
    take:
    bams


    main:
    if (params.annotation) {
        annotation_ch = Channel.fromPath(params.annotation).first()
    } else {
        DOWNLOAD_GFF()
        annotation_ch = DOWNLOAD_GFF.out.gff
    }
    FEATURE_COUNTS(bams, annotation_ch)

    MERGE_COUNTS(FEATURE_COUNTS.out.counts.map { sample, txt -> txt }.collect())
}