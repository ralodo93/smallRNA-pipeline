import os
import glob
import subprocess
import time
from utils.decorators import timer_dec
from utils.parallel import parallelize

@timer_dec(message="[DONE] Created reference index")
def make_reference(fasta_file, name = "genome"):
    print(f"[INFO] Creating reference index for {fasta_file}")
    ref_folder = os.path.dirname(fasta_file)
    os.makedirs(os.path.join(ref_folder,"bowtie"), exist_ok=True)
    bw_files = glob.glob(f"{ref_folder}/bowtie/{name}*")
    if len(bw_files) == 0:
        os.system(f"gunzip -kf {fasta_file}")
        cmd = [
            "bowtie-build",
            fasta_file.replace(".gz", ""),
            f"{ref_folder}/bowtie/{name}",
            "--threads", "10"
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.system(f"rm {fasta_file.replace('.gz','')}")
    index = f"{ref_folder}/bowtie/{name}"
    return index
    


def bowtie_wrapper(args):
    sample_name, fastq_file, index, bam_folder, log_file = args
    bam_file = f"{bam_folder}/{sample_name}.bam"
    bam_file_tmp = f"{bam_folder}/{sample_name}_tmp.bam"
    sam_file = f"{bam_folder}/{sample_name}.sam"
    if not os.path.exists(bam_file):
        start_time = time.time()
        cmd = [
            "bowtie",
            "-p", "10",
            "-n", "0",
            "-l", "18",
            "--best",
            "--nomaqround",
            "-e", "70",
            "-k", "1",
            "-S",
            "-x", index,
            fastq_file,
        ]
        with open(sam_file, "w") as out_sam:
            with open(log_file, "w") as out_log:
                subprocess.run(cmd, stdout=out_sam, stderr=out_log, text=True)
        
        cmd = [
            "samtools",
            "view",
            "--threads", "10", 
            "-bS", sam_file, "-o", bam_file_tmp
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        cmd = [
            "samtools",
            "sort",
            "--threads", "10",
            "-o", bam_file,
            bam_file_tmp
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        os.remove(sam_file)
        os.remove(bam_file_tmp)
        g_log_file = log_file.replace("_bowtie.log", ".log")
        with open(log_file, "r") as log_in:
            with open(g_log_file, "a") as log_out:
                for line in log_in:
                    if line.startswith("# reads with at least one alignment:"):
                        log_out.write(f"Reads aligned: {line.split(': ')[1].split(' ')[0]}\n")
        timer_log_file = log_file.replace("_bowtie.log", "_timer.log")
        end_time = time.time()
        with open(timer_log_file, "a") as log_out:
            log_out.write(f"bowtie_time: {end_time - start_time:.2f} seconds\n")
    return {sample_name: bam_file}

@timer_dec(message="[DONE] Bowtie alignment")
def run_bowtie(sample_dict, index, bam_folder, log_dir, ncores):
    print(f"[INFO] Running Bowtie alignment in {bam_folder}")
    args = [(sample, sample_dict[sample], index, bam_folder, f"{log_dir}/{sample}_bowtie.log") for sample in sample_dict]
    results = parallelize(bowtie_wrapper, args, ncores)
    results = {k: v for d in results for k, v in d.items()}
    return results