include { MULTIQC } from '../modules/multiqc'

workflow RUN_MULTIQC {
    take:
    fastqc_raw_ch      // *_fastqc.zip de raw
    fastqc_trimmed_ch  // *_fastqc.zip de trimmed
    trim_logs_ch       // *_cutadapt.log
    bowtie_logs_ch     // *_bowtie.log
    counts_ch          // *.txt.summary de featureCounts

    main:
    // Mezcla todos los ficheros en un único canal y espera a que estén todos
    all_files_ch = fastqc_raw_ch
        .mix(fastqc_trimmed_ch)
        .mix(trim_logs_ch)
        .mix(bowtie_logs_ch)
        .mix(counts_ch)
        .collect()   // ← espera a que todo esté listo

    MULTIQC(all_files_ch)

    emit:
    report = MULTIQC.out.report
}