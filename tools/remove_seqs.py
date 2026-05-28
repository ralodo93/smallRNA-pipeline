import dnaio
import os
import time
from utils.parallel import parallelize
from utils.decorators import timer_dec


def remove_sequences_wrapper(args):
    sample, gz_file, output_file, log_file, common_seq, umi_length, gap, adapter = args
    if not os.path.exists(output_file):
        start_time = time.time()
        
        nreads = 0
        nunique = 0
        n_common = 0
        n_umi = 0
        n_adapter = 0
        
        seqs_seen = set()
        
        short_adapter = adapter[:-gap] if gap > 0 else adapter

        # Abrimos lectura y escritura en streaming simultáneo
        with dnaio.open(gz_file, mode="r") as reader, dnaio.open(output_file, mode="w") as writer:
            for record in reader:
                nreads += 1
                
                # 1. Deduplicación al vuelo
                if record.sequence in seqs_seen:
                    continue
                seqs_seen.add(record.sequence)
                nunique += 1
                
                # Pasamos el record por el pipeline de filtrado y recorte
                # Optimizamos los pasos integrando la lógica para evitar sub-funciones y accesos a diccionarios
                sequence = record.sequence
                cut_index = sequence.find(common_seq)
                if cut_index <= 10:  # Si el common_seq no está o está muy cerca del inicio, lo descartamos
                    continue
                n_common += 1
                
                umi_start = cut_index + len(common_seq)
                if umi_start + umi_length > len(sequence): # Si no hay suficiente espacio para el UMI, lo descartamos
                    continue
                n_umi += 1
                
                # Buscar el adaptador a partir del final del UMI ahorra tiempo de CPU
                if sequence.find(short_adapter, umi_start + umi_length) == -1:
                    continue
                n_adapter += 1
                
                # Si llegó aquí, pasó todos los filtros. Recortamos y escribimos.
                record.sequence = sequence[:cut_index]
                record.qualities = record.qualities[:cut_index]
                writer.write(record)

        # Escritura de Logs
        with open(log_file, "w") as log:
            log.write(f"Total reads: {nreads}\n")
            log.write(f"Unique reads: {nunique}\n")
            log.write(f"Reads with common sequence: {n_common}\n")
            log.write(f"Reads with UMI: {n_umi}\n")
            log.write(f"Reads with adapter: {n_adapter}\n")
            
        timer_log_file = log_file.replace(".log", "_timer.log")
        end_time = time.time()
        with open(timer_log_file, "a") as log:
            log.write(f"remove_sequences_time: {end_time - start_time:.2f} seconds\n")
            
    return {sample: output_file}


@timer_dec(message="[DONE] Removed common sequence, UMIs and adapters")
def remove_sequences(sample_dict, filtered_dir, log_dir, common_seq="AACTGTAGGCACCATCAAT", umi_length=12, gap=3, adapter="AGATCGGAAGAG", ncores=2):
    print(f"[INFO] Removing common sequence, UMIs and adapters in {filtered_dir}")
    args = []
    for sample, gz_file in sample_dict.items():
        output_file = f"{filtered_dir}/{sample}.fastq.gz"
        log_file = f"{log_dir}/{sample}.log"
        args.append((sample, gz_file, output_file, log_file, common_seq, umi_length, gap, adapter))
        
    results = parallelize(remove_sequences_wrapper, args, ncores)
    
    # Unir diccionarios de salida
    return {k: v for d in results for k, v in d.items()}