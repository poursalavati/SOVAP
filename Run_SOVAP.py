import argparse
import os
import subprocess
import time
import sys 
import subprocess
from collections import defaultdict
import base64

HELP_MESSAGE = "\033[32mSOVAP: Soil Virome Analysis Pipeline v.1.3\033[0m\n\n\033[33mThis pipeline utilizes a suite of state-of-the-art tools for processing, analysis, and annotation of viromics and metagenomics data\033[0m\n"


def run_fastp(input_r1, input_r2, output_r1, output_r2, output_ru1, output_ru2, threads):

  # Creating output directory
  output_dir = "1_Fastp_Output"
  output_dir2 = "1_Fastp_Report"
  os.makedirs(output_dir, exist_ok=True)
  os.makedirs(output_dir2, exist_ok=True)
  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run Fastp
  command = f"fastp -i {input_r1} -I {input_r2} -o {output_dir}/{output_r1} -O {output_dir}/{output_r2} --unpaired1 {output_dir}/{output_ru1} --unpaired2 {output_dir}/{output_ru2} -h {output_dir2}/fastp.html -j {output_dir2}/fastp.json -w {threads} --detect_adapter_for_pe -3 --cut_window_size=1 --cut_mean_quality=15 --correction"

  # Running Fastp and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/fastp.stdout.log", "w") as stdout_file, open(f"{log_dir}/fastp.stderr.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time and returning the output files
  print(f"\033[92mFastp completed in {end_time - start_time:.2f} seconds.\033[0m")
  return f"{output_dir}/{output_r1}", f"{output_dir}/{output_r2}", f"{output_dir}/{output_ru1}", f"{output_dir}/{output_ru2}"

def run_centrifuge(input_file1, input_file2, input_file3, input_file4, output_file1, output_file2, output_file3, output_file4, centrifuge_db, threads):

  # Creating output directory
  output_dir = "2_Centrifuge_Output"
  output_dir2 = "2_CleanReads"
  os.makedirs(output_dir, exist_ok=True)
  os.makedirs(output_dir2, exist_ok=True)
  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run Centrifuge
  command = f"centrifuge -x {centrifuge_db} -1 {input_file1} -2 {input_file2} -U {input_file3} -U {input_file4} --report-file {output_dir}/{output_file1} -S {output_dir}/{output_file2} --un-conc-gz {output_dir2}/{output_file3} --un-gz {output_dir2}/{output_file4} --min-hitlen 50 --threads {threads}"

  # Running Centrifuge and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/centrifuge.stdout.log", "w") as stdout_file, open(f"{log_dir}/centrifuge.stderr.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time
  print(f"\033[92mCentrifuge completed in {end_time - start_time:.2f} seconds.\033[0m")

def run_mega(input_file1, input_file2, input_file3, threads):

  # Creating output directory
  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run Megahit
  command = f"megahit -1 {input_file1} -2 {input_file2} -r {input_file3} --presets meta-large -o 3_Megahit_Output -t {threads} --min-contig-len 150"

  # Running Megahit and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/megahit.stdout.log", "w") as stdout_file, open(f"{log_dir}/megahit.stderr.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time
  print(f"\033[92mMegahit completed in {end_time - start_time:.2f} seconds.\033[0m")

def run_geno(input_file1, genomad_db, threads):

  # Creating output directory
  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run geNomad
  #(use --disable-nn-classification to run faster)
  command = f"genomad end-to-end --cleanup -t {threads} -s 7.0 {input_file1} 4_geNomad_Output {genomad_db}"
  
  # Running geNomad and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/geNomad.stdout.log", "w") as stdout_file, open(f"{log_dir}/geNomad.stderr.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time
  print(f"\033[92mgeNomad completed in {end_time - start_time:.2f} seconds.\033[0m")

def run_diamond(input_file1, diamond_db, output, un, al, threads):

  # Creating output directory
  output_dir = "6_Diamond-Taxonomy"
  os.makedirs(output_dir, exist_ok=True)

  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run DIAMOND
  command = f"diamond blastx -q {input_file1} -d {diamond_db} -o {output_dir}/{output} -f 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send qlen slen stitle evalue bitscore -k 1 --sensitive -p {threads} --alfmt fasta --al {output_dir}/{al} --unfmt fasta --un {output_dir}/{un}"

  # Running DIAMOND and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/diamond.stdout.log", "w") as stdout_file, open(f"{log_dir}/diamond.stderr.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time
  print(f"\033[92mDiamond on IMG/VR completed in {end_time - start_time:.2f} seconds.\033[0m")

def run_diamegan(input_file1, diamond_db, output, un, al, megan_db, threads):

  # Creating output directory
  output_dir = "6_Diamond_Megan"
  os.makedirs(output_dir, exist_ok=True)

  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run Diamond+Megan
  command1 = f"diamond blastx -q {input_file1} -d {diamond_db} -o {output_dir}/{output} -f 100 -k 1 --sensitive -p {threads} --alfmt fasta --al {output_dir}/{al} --unfmt fasta --un {output_dir}/{un}"
  command2 = f"daa-meganizer -i {output_dir}/{output} -t {threads} -mdb {megan_db}"
  command = f"{command1}; {command2}"
  

  # Running D-M and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/Diamond-Megan.stdout.log", "w") as stdout_file, open(f"{log_dir}/Diamond-Megan.stderr.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time
  print(f"\033[92mDiamond + Megan completed in {end_time - start_time:.2f} seconds.\033[0m")


def run_tpm(input_file1, mem, threads):

  # Creating output directory
  output_dir = "5_Clusters_Abundance"
  os.makedirs(output_dir, exist_ok=True)
  # Creating output directory
  # Creating log directory
  log_dir = "0_Logs"
  os.makedirs(log_dir, exist_ok=True)

  # Defining the command to run TPM and CD-HIT
  command1 = f"seqkit seq -m 500 {input_file1} -o 5_Clusters_Abundance/virus_contig_500.fa -j {threads}"
  command2 = f"cd-hit -i 5_Clusters_Abundance/virus_contig_500.fa -c 0.95 -G 0 -aS 0.75 -T {threads} -M {mem} -o 5_Clusters_Abundance/virus_contig_500_clustered.fasta"
  command3 = f"cat 1_Fastp_Output/* > 1_Fastp_Output/Cat_Trimmed.fq.gz"
  command4 = f"bwa index 5_Clusters_Abundance/virus_contig_500_clustered.fasta"
  command5 = f"bwa mem -t {threads} 5_Clusters_Abundance/virus_contig_500_clustered.fasta 1_Fastp_Output/Cat_Trimmed.fq.gz -o 5_Clusters_Abundance/mapped.sam"
  command6 = f"samtools sort --threads {threads} -O SAM 5_Clusters_Abundance/mapped.sam -o 5_Clusters_Abundance/sorted.mapped.sam"
  command7 = f"rm 5_Clusters_Abundance/mapped.sam"
  command = f"{command1}; {command2}; {command3}; {command4}; {command5}; {command6}; {command7}"
  
  # Running TPM and CD-HIT and capturing stdout and stderr
  start_time = time.time()
  with open(f"{log_dir}/Clusters_Abundance.stdout.log", "w") as stdout_file, open(f"{log_dir}/Clusters_Abundance.log", "w") as stderr_file:
      process = subprocess.Popen(command, stdout=stdout_file, stderr=stderr_file, shell=True)
      process.wait()
  end_time = time.time()

  # Printing the execution time
  print(f"\033[92mClustering and mapping completed in {end_time - start_time:.2f} seconds.\033[0m")

def calc_abundance(sam_file):
    # Define the counts dictionary to store the read counts for each contig
    counts = defaultdict(int)

    # Get the length of each contig from the SAM file using samtools
    contig_lengths = {}
    with subprocess.Popen(['samtools', 'view', '-H', sam_file], stdout=subprocess.PIPE) as proc:
        for line in proc.stdout:
            if line.startswith(b'@SQ'):
                fields = line.decode().split('\t')
                contig_id = fields[1].split(':')[1]
                contig_len = int(fields[2].split(':')[1])
                contig_lengths[contig_id] = contig_len

    # Parse the SAM file with samtools to count the reads mapped to each contig
    with subprocess.Popen(['samtools', 'idxstats', sam_file], stdout=subprocess.PIPE) as proc:
        for line in proc.stdout:
            fields = line.decode().split('\t')
            contig_id = fields[0]
            if contig_id not in contig_lengths:
                continue
            contig_len = contig_lengths[contig_id]
            count = int(fields[2])
            counts[contig_id] = count

    # Calculate the total count per million
    cpm_factor = 1e6 / sum(counts.values())
    tpm_factor = 1e6 / sum([count/contig_lengths[contig_id] for contig_id, count in counts.items()])
    fpkm_factor = 1e9 / sum(counts.values())

    # Write the abundance values to a file
    with open('5_Clusters_Abundance/abundance.tsv', 'w') as outfile:
        outfile.write('contig_id\tcount\tcpm\ttpm\tfpkm\tlength\n')
        for contig_id, count in counts.items():
            # Calculate the CPM value
            cpm = count * cpm_factor
            # Calculate the TPM value
            tpm = count / contig_lengths[contig_id] * tpm_factor
            # Calculate the FPKM value
            fpkm = (count / contig_lengths[contig_id]) * fpkm_factor
            # Write the abundance values for the contig to the file
            outfile.write(f'{contig_id}\t{count}\t{cpm:.2f}\t{tpm:.2f}\t{fpkm:.2f}\t{contig_lengths[contig_id]}\n')

base64_str = "XG5CeSBBYmRvbmFzZXIgUG91cnNhbGF2YXRpXG5Eci4gRmFsbCBWaXJvbG9neSBsYWIgMjAyMiAtIDIwMjNcblxuXDAzM1s5MW1BZ3JpY3VsdHVyZSBhbmQgQWdyaS1Gb29kIENhbmFkYSAoQUFGQylcbkFncmljdWx0dXJlIGV0IEFncm9hbGltZW50YWlyZSBDYW5hZGEgKEFBQylcMDMzWzBtXG5cMDMzWzk2bUFiZG9uYXNlci5Qb3Vyc2FsYXZhdGlAYWdyLmdjLmNhXDAzM1swbVxuXG5cMDMzWzkybUJpb2xvZ3kgRGVwYXJ0bWVudCwgVW5pdmVyc2l0ZSBkZSBTaGVyYnJvb2tlIChVZFMpXDAzM1swbVxuXDAzM1s5Nm1Qb3Vyc2FsYXZhdGkuQWJkb25hc2VyQFVzaGVyYnJvb2tlLmNhXDAzM1swbVxuXHQ="
version_str = base64.b64decode(base64_str).decode('unicode_escape')

base64_str3 = "4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paECuKWiOKWiOKWkeKWhOKWhOKWhOKWkeKWiOKWiOKWkeKWhOKWhOKWhOKWkeKWiOKWiOKWkeKWiOKWiOKWiOKWkeKWiOKWkeKWhOKWhOKWgOKWiOKWiOKWkeKWhOKWhOKWkeKWiOKWiArilojilojiloTiloTiloTiloDiloDilojilojilpHilojilojilojilpHilojilojilojilpHilojilpHilojilojilpHiloDiloDilpHilojilojilpHiloDiloDilpHilojilogK4paI4paI4paR4paA4paA4paA4paR4paI4paI4paR4paA4paA4paA4paR4paI4paI4paI4paE4paA4paE4paI4paI4paR4paI4paI4paR4paI4paI4paR4paI4paI4paI4paI4paICuKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgA=="
so = base64.b64decode(base64_str3).decode()

base64_str2 = "4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGACuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKivuKjv+KhhuKhgOKhgOKhgOKhgOKisOKjtuKhhuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgArioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDio6DioYTioIjio7/ioYHioYDioLjioZ/ioYDiorjioZ/ioIHiooDioYDioYDioYDioYDioYDioYDioYDiorjio7/ioYDioYDioYDioYDioYDioYDioYAK4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qKg4qO/4qO/4qGA4qGA4qKI4qOj4qOk4qG/4qC34qC/4qC/4qC/4qC24qC+4qKm4qOE4qO84qCB4qGA4qGA4qGA4qGA4qGA4qGA4qK44qO/4qGA4qGA4qGA4qGA4qGA4qGA4qGACuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKjgOKgiOKgmeKjt+KjtuKgn+Kgi+KhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKgieKggeKhgOKhgOKhgOKhgOKhgOKhgOKiuOKjv+KhgOKhgOKhgOKhgOKhgOKhgOKhgArioYDioYDioYDio6Dio6TioYDioIjioJviorPio77ioJ/ioIHiorjio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYfioYDioYDioYDioYDioYDioYDiorjio7/ioYDioYDioYDioYDioYDioYDioYAK4qGA4qGA4qGA4qC74qC/4qC34qOk4qOk4qG/4qCB4qGA4qGA4qK44qO/4qO/4qO/4qGf4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCD4qGA4qGA4qGA4qGA4qGA4qGA4qC44qC/4qC24qC24qC24qC24qCG4qGA4qGACuKhgOKhgOKhgOKhgOKjpOKjhOKjoOKjv+KggeKhgOKhgOKhgOKiuOKjv+Kjv+Kjv+Khh+KhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKjoOKjpOKjpOKjpOKhgOKhgOKhgOKhgArioYDioYDiooDio4DioInioIHiorjioYfioYDioYDioYDioYDiorjio7/io7/io7/io7fio7bio7bio7bio7bio7bio7bio7bioYDioYDioYDioYDioYDioYDioYDioYDioYDioInioIHioYDioonio7/ioYbioYDioYAK4qGA4qGA4qK/4qO/4qC34qC24qK/4qGH4qGA4qGA4qGA4qGA4qK44qO/4qO/4qO/4qG/4qC/4qC/4qC/4qC/4qC/4qC/4qC/4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qKg4qG+4qCb4qCL4qCJ4qO/4qGH4qGA4qGACuKhgOKhgOKhgOKhgOKjoOKjpOKivOKjt+KhgOKhgOKhgOKhgOKiuOKjv+Kjv+Kjv+Khh+KhgOKhgOKhgOKhgOKjtuKhgOKjtuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKiu+Kjp+KjgOKjgOKjoOKjv+Khh+KhgOKhgArioYDioYDioYDioYDioInioIHioYDiorvio6bioYDioYDioYDiorjio7/io7/io7/ioYfioLrio5vio7/ioYDio7/ioYDio7/ioYDioYDioYDioYDioYDioYDioYDioYDioYDioInioInioInioIHioInioIHioYDioYAK4qGA4qGA4qGA4qKg4qO24qO24qG24qCb4qC74qOn4qGA4qGA4qK44qO/4qO/4qO/4qGH4qO/4qOp4qO/4qGA4qO/4qGA4qO/4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qK44qGH4qGA4qGA4qGA4qGA4qGA4qGA4qGACuKhgOKhgOKhgOKgiOKgm+Kgi+KhgOKjpOKhnuKgmeKiv+KjpuKjjOKgieKgieKgieKggeKgiOKggeKgiOKhgOKgieKhgOKgieKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKiuOKjh+KjoOKjtOKjpuKjhOKhgOKhgOKhgArioYDioYDioYDioYDioYDioYDioYDioIniooDio6Diob7ioIvioLviob/io7bio7bio6Tio6Tio4Tio4Dio6Dio6Tio6Tio7bioJbioYDioYDioYDioYDioYDioYDioYDiorjioY/ioIHioYDioYDiorvio4fioYDioYAK4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qO/4qO/4qCB4qKg4qO+4qGA4qGA4qKI4qG/4qCJ4qK/4qCJ4qCZ4qO/4qGA4qCI4qOm4qGE4qGA4qGA4qGA4qGA4qGA4qGA4qK44qGH4qGA4qGA4qGA4qK44qG/4qGA4qGACuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKioOKjvuKhh+KhgOKgv+KghuKhgOKjv+Kjp+KhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKiuOKjp+KjhOKjgOKjpOKhv+Kgg+KhgOKhgArioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioIjioJvioIPioYDioYDioYDioYDioJvioJvioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioIjioInioIHioYDioYDioYDioYAKCiA="

lo_str = base64.b64decode(base64_str2).decode()

epi="\033[91mFor updated versions and information, please visit:\033[0m \033[92mhttps://github.com/poursalavati/SOVAP \033[0m\n\033[91mIf you find SOVAP useful, please kindly cite:\033[0m\033[92m DOI.org/10.5281/zenodo.7700081\033[0m\n\033[91mFor questions and bugs please contact:\033[0m \033[92mAbdonaser.Poursalavati@agr.gc.ca\033[0m"

def main():
  print(so)
  print(HELP_MESSAGE)
  # Parsing arguments
  parser = argparse.ArgumentParser(description="SOVAP Help Menu", formatter_class=argparse.RawTextHelpFormatter, epilog=epi)
  parser.add_argument("-r1", "--read1", metavar="", required=True, help="Path to R1 FASTQ file")
  parser.add_argument("-r2", "--read2", metavar="", required=True, help="Path to R2 FASTQ file")
  parser.add_argument("-x", "--centrifuge_db", metavar="", required=True, help="Path to the Centrifuge database")
  parser.add_argument("-g", "--geNomad_db", metavar="", required=True, help="Path to the geNomad database")
  parser.add_argument("-d", "--diamond_db", metavar="", required=True, help="Path to the Diamond database")
  parser.add_argument("-md", "--megan_db", metavar="", help="Path to the Megan database")
  parser.add_argument("-t", "--threads", metavar="", type=int, default=16, help="Number of threads to use (default: 16)")
  parser.add_argument("-m", "--mem", metavar="", type=int, default=16000, help="MB of memory to use (default: 16000)")
  parser.add_argument("--end_to_end", action="store_true", help="Run the entire pipeline end-to-end")
  parser.add_argument("--megan", action="store_true", help="Run Diamond and Megan with NCBI db")
  parser.add_argument('-v', '--version', action='version', version='{}\n{}\n'.format(version_str, lo_str), help='Print version, affiliation, and contact information')
  args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
  
  
    
# Running the pipeline
  if args.end_to_end:
      tstart_time = time.time()
      ttstart_time = time.time()
      print("Running the pipeline end-to-end...")

    # Running Fastp
      print("\033[94m:::> Start Module 1: Trimming and pre-processing raw data <:::\033[0m")
      # Check if output files exist
      if not os.path.exists("1_Fastp_Output"):
        # Run Fastp
          fastp_output_r1, fastp_output_r2, fastp_output_ru1, fastp_output_ru2 = run_fastp(args.read1, args.read2, "output_r1.fastq.gz", "output_r2.fastq.gz", "output_ru1.fastq.gz", "output_ru2.fastq.gz", args.threads)
      else:
          print(f"Skipping this step because output already exists")
    # Running Centrifuge
      print("\033[94m:::> Start Module 2: Contamination subtraction (Bacteria and Archaea classification) <:::\033[0m")
      # Check if output files exist
      if not os.path.exists("2_CleanReads"):
      # Run Centrifuge
          run_centrifuge(fastp_output_r1, fastp_output_r2, fastp_output_ru1, fastp_output_ru2, "output.centrifuge.report", "output.centrifuge.tsv", "output.centrifuge_paired_%.fq.gz", "output.centrifuge_unpaired.fq.gz", args.centrifuge_db, args.threads)
      else:
          print(f"Skipping this step because output already exists")
      
      # Running Megahit
      print("\033[94m:::> Start Module 3: Assembly of cleaned reads <:::\033[0m")
      # Check if output files exist
      if not os.path.exists("3_Megahit_Output"):
      
          run_mega("2_CleanReads/output.centrifuge_paired_1.fq.gz", "2_CleanReads/output.centrifuge_paired_2.fq.gz", "2_CleanReads/output.centrifuge_unpaired.fq.gz", args.threads)
      else:
          print(f"Skipping this step because output already exists")

      # Running geNomad
      print("\033[94m:::> Start Module 4: Identification of viral contigs <:::\033[0m")
      # Check if output files exist
      if not os.path.exists("4_geNomad_Output"):
      
          run_geno("3_Megahit_Output/final.contigs.fa", args.geNomad_db, args.threads)
      else:
          print(f"Skipping this step because output already exists")
          
      # Running Clustering and Mapping
      print("\033[94m:::> Start Module 5: Clustering and mapping <:::\033[0m")
      # Check if output files exist
      if not os.path.exists("5_Clusters_Abundance"):
      
          run_tpm("4_geNomad_Output/final.contigs_summary/final.contigs_virus.fna", args.mem, args.threads)
      else:
          print(f"Skipping this step because output already exists")
      
      # Running Abundance
      print("\033[94m:::> Start Module 5.1: Abundance and TPM estimation <:::\033[0m")
      # Check if output files exist
      if not os.path.exists("5_Clusters_Abundance/abundance.tsv"):
          start_time = time.time()
          calc_abundance("5_Clusters_Abundance/sorted.mapped.sam")
          end_time = time.time()
  # Printing the execution time
          print(f"\033[92mAbundance estimation completed in {end_time - start_time:.2f} seconds.\033[0m")
      else:
          print(f"Skipping this step because output already exists")
      # Running IMGVR diamond
      if not args.megan:
          print("\033[94m:::> Start Module 6: Taxonomy assignment <:::\033[0m")
          # Check if output files exist
          if not os.path.exists("6_Diamond-Taxonomy"):
      
              run_diamond("5_Clusters_Abundance/virus_contig_500_clustered.fasta", args.diamond_db, "output.diamond.tsv", "unaligned.diamond.fa", "aligned.diamond.fa", args.threads)
              ttend_time = time.time()
              print(f"\n\033[92mSOVAP pipeline finished in {ttend_time - ttstart_time:.2f} seconds.\033[0m\nPlease look at '0_Logs' folder to access the logs of each step\n")
          else:
              print(f"Skipping this step because output already exists")
      else:
    # Running Diamond+Megan
        print("\033[94m:::> Start Module 6: Diamond + Megan Analysis <:::\033[0m")
      # Check if output files exist
        if not os.path.exists("6_Diamond_Megan"):
      # Run Diamond-Megan
            run_diamegan("5_Clusters_Abundance/virus_contig_500_clustered.fasta", args.diamond_db, "output.diamond.daa", "unaligned.diamond.fa", "aligned.diamond.fa", args.megan_db, args.threads)
        else:
            print(f"Skipping this step because output already exists")
        tend_time = time.time()
        print(f"\n\033[92mSOVAP pipeline finished in {tend_time - tstart_time:.2f} seconds.\033[0m\nPlease look at '0_Logs' folder to access the logs of each step\n")
  else:
    # Running Fastp only
      print("Running Fastp...")
      fastp_output_r1, fastp_output_r2 = run_fastp(args.read1, args.read2, "output_r1.fastq", "output_r2.fastq", args.threads)

    # Running Centrifuge only
      print("Running Centrifuge...")
      run_centrifuge(fastp_output_r1, "output.centrifuge.report", args.centrifuge_db, args.threads)
if __name__ == "__main__":
    main()
