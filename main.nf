nextflow.enable.dsl=2

def validateParams() {
    def errors = []

    if (!params.input)
        errors << "--input is required and should point to the samplesheet CSV file (e.g., --input samplesheet.csv)"
    
    if (!params.index) {
        if (!params.fasta_url)
            errors << "--fasta_url is required if --index is not provided"
        if (!params.index_name)
            errors << "--index_name is required if --index is not provided"
    }


    if (errors) {
        log.error """
        ============================================
        ERROR: missing required parameters
        ============================================
        ${errors.join('\n        ')}
        ============================================
        """.stripIndent()
        System.exit(1)
    }
}

def validateSamplesheet(csv_path) {
    def required_cols = ["sample", "fastq"]
    def header = file(csv_path).readLines().first().split(",")*.trim()
    def missing = required_cols.findAll { !(it in header) }
    if (missing) {
        log.error "El samplesheet no tiene las columnas: ${missing.join(', ')}"
        System.exit(1)
    }
}


include { PREPROCESSING } from './subworkflows/preprocessing'
include { PREPARE_GENOME } from './subworkflows/prepare_genome'
include { ALIGNMENT } from './subworkflows/alignment'
include { GET_COUNTS } from './subworkflows/get_counts'

workflow {

    validateParams()

    // Leer el CSV y crear el canal con [nombre_muestra, fichero]
    reads_ch = Channel
        .fromPath(params.input)
        .splitCsv(header: true)
        .map { row -> tuple(row.sample, file(row.fastq)) }

    // Preprocessing workflow
    PREPROCESSING(reads_ch)

    // PREPARE GENOME
    // Si ya existe el índice, lo carga; si no, lo construye
    if (params.index) {
    // Caso 1: se proporcionó --index directamente
        log.info "Using existing index: ${params.index}"
        index_files_ch = Channel.fromPath("${params.index}*.ebwt").collect().first()
        index_name_ch  = Channel.value(params.index.split('/')[-1])  // deriva el nombre del path
    } else {
        // Caso 2 y 3: se proporcionó --fasta_url e --index_name
        def default_index = "${params.genomedir}/${params.index_name}/${params.index_name}"
        def index_exists  = file("${default_index}.1.ebwt").exists()

        if (index_exists) {
            // Caso 2: el índice ya existe en la ruta por defecto → lo usa directamente
            log.info "Index already exists at ${default_index}, skipping PREPARE_GENOME"
            index_files_ch = Channel.fromPath("${default_index}*.ebwt").collect().first()
            index_name_ch  = Channel.value(params.index_name)

        } else {
            // Caso 3: no existe → descarga y construye
            log.info "Building index from ${params.fasta_url}"
            PREPARE_GENOME()
            index_files_ch = PREPARE_GENOME.out.ebwt_files
            index_name_ch  = PREPARE_GENOME.out.prefix
        }
    }

    // Alignment workflow
    ALIGNMENT(PREPROCESSING.out.trimmed, index_files_ch, index_name_ch)

    // Get counts workflow
    GET_COUNTS(ALIGNMENT.out.bam)
}