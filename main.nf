nextflow.enable.dsl=2

params.threads  = 4
params.input    = "samplesheet.csv"      // ← ahora apunta al CSV
params.outdir   = "results"
params.fasta_url  = "https://ftp.ensembl.org/pub/release-113/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.22.fa.gz"
params.genomedir  = "reference"
params.index_name = "chr22"
params.index = null
params.annotation_url = "https://mirbase.org/download/hsa.gff3"
params.annotation = null

include { PREPROCESSING } from './subworkflows/preprocessing'
include { PREPARE_GENOME } from './subworkflows/prepare_genome'
include { ALIGNMENT } from './subworkflows/alignment'
include { GET_COUNTS } from './subworkflows/get_counts'

workflow {

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
        index_files_ch = Channel.fromPath("${params.index}*.ebwt").collect().first()
        index_name_ch  = Channel.value(params.index_name)
    } else {
        PREPARE_GENOME()
        index_files_ch = PREPARE_GENOME.out.ebwt_files
        index_name_ch  = PREPARE_GENOME.out.prefix
    }

    // Alignment workflow
    ALIGNMENT(PREPROCESSING.out.trimmed, index_files_ch, index_name_ch)

    // Get counts workflow
    GET_COUNTS(ALIGNMENT.out.bam)
}