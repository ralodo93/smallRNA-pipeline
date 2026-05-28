import os
import subprocess
import dnaio
import time
from utils.parallel import parallelize
from utils.decorators import timer_dec

def count_reads(gz_file):
    nreads = 0
    # dnaio maneja la descompresión y el formato FASTQ automáticamente (en bloques internos de C)
    with dnaio.open(gz_file, mode="r") as fastq:
        for record in fastq:
            nreads += 1
    return nreads

def cutadapt_wrapper(args):
    sample, r1_file, output_dir, log_file = args
    out_path = f"{output_dir}/{sample}.fastq.gz"
    if not os.path.exists(out_path):
        start_time = time.time()
        cmd = ["cutadapt", "-j", "10", "-m", "10", "-M", "50", "-o", out_path, r1_file]
        with open(log_file, "w") as log_out:
            subprocess.run(cmd, stdout=log_out, stderr=subprocess.STDOUT)
        nreads = count_reads(out_path)
        with open(log_file.replace("_cutadapt.log", ".log"), "a") as log_out:
            log_out.write(f"Reads cleaned: {nreads}\n")
        end_time = time.time()
        timer_log_file = log_file.replace("_cutadapt.log", "_timer.log")
        with open(timer_log_file, "a") as log_out:
            log_out.write(f"cutadapt_time: {end_time - start_time:.2f} seconds\n")
    return {sample: out_path}

@timer_dec(message="[DONE] Cutadapt trimming")
def run_cutadapt(sample_dict, output_dir, log_dir, ncores):
    print(f"[INFO] Running Cutadapt trimming in {output_dir}")
    args = [(sample, sample_dict[sample], output_dir, f"{log_dir}/{sample}_cutadapt.log") for sample in sample_dict]
    results = parallelize(cutadapt_wrapper, args, ncores)
    results = {k: v for d in results for k, v in d.items()}
    return results