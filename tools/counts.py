import pandas as pd
from utils.parallel import parallelize
from utils.decorators import timer_dec
import subprocess
import os
import time

def feature_counts_wrapper(args):
    sample_name, bam_file, gff_file, output_folder, log_file = args
    output_file = f"{output_folder}/{sample_name}_feature_counts.txt"
    if not os.path.exists(output_file):
        start_time = time.time()
        cmd = [
            "featureCounts",
            "-T", "10", "-t", "miRNA", "-g", "Name",
            "-s", "1", "-O",
            "-a", gff_file,
            "-o", output_file,
            bam_file
        ]
        with open(log_file, "w") as out_log:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=out_log)
        g_log_file = log_file.replace("_feature_counts.log", ".log")
        with open(log_file, "r") as log_in:
            with open(g_log_file, "a") as log_out:
                for line in log_in:
                    if line.startswith("||    Successfully assigned alignments :"):
                        log_out.write(f"Reads assigned: {line.split(': ')[1].split(' ')[0]}\n")
        log_timer_file = log_file.replace("_feature_counts.log", "_timer.log")
        end_time = time.time()
        with open(log_timer_file, "a") as log_out:
            log_out.write(f"feature_counts_time: {end_time - start_time:.2f} seconds\n")
    return {sample_name: output_file}

@timer_dec(message="[DONE] Feature counting")
def run_feature_counts(bam_sample_dict, gff_file, output_folder, log_folder, ncores):
    print(f"[INFO] Running featureCounts in {output_folder}")
    args = [(sample, bam_sample_dict[sample], gff_file, output_folder, f"{log_folder}/{sample}_feature_counts.log") for sample in bam_sample_dict]
    results = parallelize(feature_counts_wrapper, args, ncores)
    results = {k: v for d in results for k, v in d.items()}
    return results


def merge_counts(counts_dict, counts_dir):
    output_file = f"{counts_dir}/merged_counts.csv"
    all_dfs = []
    for sample_name in counts_dict:
        counts_file = counts_dict[sample_name]
        sample_name = sample_name.replace("-", "_")
        df = pd.read_csv(counts_file, sep="\t", comment="#", header=0)
        df = df.rename(columns={df.columns[-1]: sample_name})
        df = df[["Geneid", sample_name]]
        df.columns = ["miRNA", sample_name]
        df.set_index("miRNA", inplace=True)
        all_dfs.append(df)
    merged_df = pd.concat(all_dfs, axis=1, join="outer").fillna(0).astype(int)
    merged_df.to_csv(output_file)