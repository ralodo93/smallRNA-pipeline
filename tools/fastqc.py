import subprocess
import glob
import time
from utils.parallel import parallelize
from utils.decorators import timer_dec

def fastqc_wrapper(args):
    sample, r1_file, output_dir, log_file = args
    cmd = ["fastqc", "-t", "4", r1_file, "-o", output_dir]
    fastqc_files = glob.glob(f"{output_dir}/{sample}_*")
    if len(fastqc_files) == 0:
        start_time = time.time()
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        end_time = time.time()
        with open(log_file, "a") as log:
            log.write(f"fastqc_time: {end_time - start_time:.2f} seconds\n")
        
    
@timer_dec(message="[DONE] FASTQ quality control")
def run_fastqc(sample_dict, output_dir, log_dir, ncores):
    print(f"[INFO] Running FASTQ quality control in {output_dir}")
    args = [(sample, sample_dict[sample], output_dir, f"{log_dir}/{sample}_timer.log") for sample in sample_dict]
    parallelize(fastqc_wrapper, args, ncores)