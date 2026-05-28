#!/usr/bin/env python3

import dnaio
import argparse

def remove_sequences(gz_file, output_file, common_seq, umi_length, adapter, gap):
    seqs_seen = set()
    short_adapter = adapter[:-gap] if gap > 0 else adapter

    with dnaio.open(gz_file, mode="r") as reader, dnaio.open(output_file, mode="w") as writer:
        for record in reader:
            if record.sequence in seqs_seen:
                continue
            seqs_seen.add(record.sequence)

            sequence = record.sequence
            cut_index = sequence.find(common_seq)
            if cut_index <= 10:
                continue
            
            umi_start = cut_index + len(common_seq)
            if umi_start + umi_length > len(sequence):
                continue
            
            if sequence.find(short_adapter, umi_start + umi_length) == -1:
                continue
            
            record.sequence = sequence[:cut_index]
            record.qualities = record.qualities[:cut_index]
            writer.write(record)

def parse_args():
    parser = argparse.ArgumentParser(description="Filter and trim reads based on common sequence, UMI, and adapter presence.")
    parser.add_argument("--input", "-i", help="Input gzipped FASTQ file", required=True)
    parser.add_argument("--output", "-o", help="Output gzipped FASTQ file", required=True)
    parser.add_argument("--common_seq", default="AACTGTAGGCACCATCAAT", help="Common sequence to search for")
    parser.add_argument("--umi_length", type=int, default=12, help="Length of the UMI")
    parser.add_argument("--adapter", default="AGATCGGAAGAG", help="Adapter sequence to search for")
    parser.add_argument("--gap", type=int, default=0, help="Number of bases to allow as gap in the adapter (default: 0)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    remove_sequences(args.input, args.output, args.common_seq, args.umi_length, args.adapter, args.gap)