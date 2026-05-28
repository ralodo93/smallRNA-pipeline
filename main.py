from utils.dict import fastq_dict, summary_logs, prepare_directories
from utils.download_file import download_file
from tools.fastqc import run_fastqc
from tools.remove_seqs import remove_sequences
from tools.cutadapt import run_cutadapt
from tools.bowtie import make_reference, run_bowtie
from tools.counts import run_feature_counts, merge_counts

# conda activate mirna

if __name__ == "__main__":
    
    results_dir = "results"
    fastqc_raw_dir, log_dir, filtered_dir, trimmed_dir, fastqc_trimmed_dir, reference_dir, bam_dir, counts_dir = prepare_directories(results_dir)
    
    path = "fastq"
    sample_dict = fastq_dict(path, log_dir)
    run_fastqc(sample_dict, fastqc_raw_dir, log_dir, ncores=10)
    
    filtered_sample_dict = remove_sequences(sample_dict, filtered_dir, log_dir, common_seq = "AACTGTAGGCACCATCAAT", adapter = "AGATCGGAAGAG", umi_length=12, gap = 3, ncores=10)
    
    cutadapt_sample_dict = run_cutadapt(filtered_sample_dict, trimmed_dir, log_dir, ncores=10)
    
    run_fastqc(cutadapt_sample_dict, fastqc_trimmed_dir, log_dir, ncores=10)
    
    fasta_url = "https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"
    reference_fasta = download_file(fasta_url, reference_dir)
    index = make_reference(reference_fasta, name = "genome")
    
    bam_sample_dict = run_bowtie(cutadapt_sample_dict, index, bam_dir, log_dir, ncores=10)
    
    gff_url = "https://mirbase.org/download/hsa.gff3"
    gff_file = download_file(gff_url, reference_dir)

    feature_counts_results = run_feature_counts(bam_sample_dict, gff_file, counts_dir, log_dir, ncores=10)
    summary_logs(log_dir=log_dir)
    
    merge_counts(feature_counts_results, counts_dir)