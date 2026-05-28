import glob
import os
import pandas as pd
from utils.decorators import timer_dec

def prepare_directories(results_dir):
    fastqc_raw_dir = f"{results_dir}/fastqc_raw"
    logs_dir = f"{results_dir}/logs"
    filtered_dir = f"{results_dir}/filtered_fastq"
    trimmed_dir = f"{results_dir}/trimmed"
    fastqc_trimmed_dir = f"{results_dir}/fastqc_trimmed"
    reference_dir = "reference"
    bam_dir = f"{results_dir}/bam"
    counts_dir = f"{results_dir}/counts"
    
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(fastqc_raw_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(filtered_dir, exist_ok=True)
    os.makedirs(trimmed_dir, exist_ok=True)
    os.makedirs(fastqc_trimmed_dir, exist_ok=True)
    os.makedirs(reference_dir, exist_ok=True)
    os.makedirs(bam_dir, exist_ok=True)
    os.makedirs(counts_dir, exist_ok=True)
    
    return fastqc_raw_dir, logs_dir, filtered_dir, trimmed_dir, fastqc_trimmed_dir, reference_dir, bam_dir, counts_dir

@timer_dec(message="[DONE] Located FASTQ files")
def fastq_dict(path, log_dir):
    print(f"[INFO] Locating FASTQ files in {path}")
    fastq_files = glob.glob(f"{path}/*.fastq.gz")
    r1_files = [f for f in fastq_files if "_R1_" in f]
    r1_files = [f for f in r1_files if "Undetermined" not in f]
    r1_files_sorted = sorted(r1_files, key=os.path.getsize, reverse=True)
    sample_names = [f.split("/")[-1].split("_R1_")[0] for f in r1_files_sorted]
    sample_dict = {}
    for sample in sample_names:
        r1_file = f"{path}/{sample}_R1_001.fastq.gz"
        sample_dict[sample] = r1_file
        log_file = os.path.join(log_dir, f"{sample}_timer.log")
        if not os.path.exists(log_file):
            with open(log_file, "w") as log:
                log.write("Processing times\n")
    return sample_dict

def summary_logs(log_dir, pattern = ".log"):
    data = []
    for log_file in os.listdir(log_dir):
        if "feature_counts" not in log_file and "bowtie" not in log_file and "cutadapt" not in log_file and "timer" not in log_file and log_file.endswith(pattern):
            sample_name = log_file.split(pattern)[0]
            metrics = {"sample": sample_name}
            with open(os.path.join(log_dir, log_file), "r") as log:
                for line in log:
                    key, value = line.strip().split(": ")
                    metrics[key] = int(value)
            data.append(metrics)
    summary = pd.DataFrame(data)
    summary.set_index("sample", inplace=True)
    summary.to_csv(os.path.join(log_dir, "summary.csv"))