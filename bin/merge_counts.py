#!/usr/bin/env python3

import sys
import pandas as pd

files = sys.argv[1:]   # lista de todos los .txt

def merge_counts(files):
    all_dfs = []
    for file in files:
        sample_name = file.replace(".txt", "")
        df = pd.read_csv(file, sep="\t", comment="#", header=0)
        df = df.rename(columns={df.columns[-1]: sample_name})
        df = df[["Geneid", sample_name]]
        df.columns = ["miRNA", sample_name]
        df.set_index("miRNA", inplace=True)
        all_dfs.append(df)
    merged_df = pd.concat(all_dfs, axis=1, join="outer").fillna(0).astype(int)
    merged_df.to_csv("merged_counts.txt")

if __name__ == "__main__":
    merge_counts(files)