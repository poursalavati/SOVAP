import argparse
import os
import subprocess
import time
import sys 
import subprocess
from collections import defaultdict
import base64

# Get the directory name of the current script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the name of the external script file
script_file = "Run_SOVAP.py"

# Define the external script command with the full path of the external script file in the current folder
script_cmd = "python {}/{} -r1 {} -r2 {} -t {} -x {} --end_to_end -g {} -d {}"

HELP_MESSAGE = "\033[32mSOVAP: Soil Virome Analysis Pipeline v.1.3\033[0m\n\033[33mBy Abdonaser Poursalavati\nPoursalavati.Abdonaser@agr.gc.ca\033[0m\n\033[37mThis script loop through paired end fastq files and run SOVAP Pipeline on each set (Batch Mode)\033[0m\n\n"

base64_str = "XG5CeSBBYmRvbmFzZXIgUG91cnNhbGF2YXRpXG5Eci4gRmFsbCBWaXJvbG9neSBsYWIgMjAyMiAtIDIwMjNcblxuXDAzM1s5MW1BZ3JpY3VsdHVyZSBhbmQgQWdyaS1Gb29kIENhbmFkYSAoQUFGQylcbkFncmljdWx0dXJlIGV0IEFncm9hbGltZW50YWlyZSBDYW5hZGEgKEFBQylcMDMzWzBtXG5cMDMzWzk2bUFiZG9uYXNlci5Qb3Vyc2FsYXZhdGlAYWdyLmdjLmNhXDAzM1swbVxuXG5cMDMzWzkybUJpb2xvZ3kgRGVwYXJ0bWVudCwgVW5pdmVyc2l0ZSBkZSBTaGVyYnJvb2tlIChVZFMpXDAzM1swbVxuXDAzM1s5Nm1Qb3Vyc2FsYXZhdGkuQWJkb25hc2VyQFVzaGVyYnJvb2tlLmNhXDAzM1swbVxuXHQ="
version_str = base64.b64decode(base64_str).decode('unicode_escape')

base64_str3 = "4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paE4paECuKWiOKWiOKWkeKWhOKWhOKWhOKWkeKWiOKWiOKWkeKWhOKWhOKWhOKWkeKWiOKWiOKWkeKWiOKWiOKWiOKWkeKWiOKWkeKWhOKWhOKWgOKWiOKWiOKWkeKWhOKWhOKWkeKWiOKWiArilojilojiloTiloTiloTiloDiloDilojilojilpHilojilojilojilpHilojilojilojilpHilojilpHilojilojilpHiloDiloDilpHilojilojilpHiloDiloDilpHilojilogK4paI4paI4paR4paA4paA4paA4paR4paI4paI4paR4paA4paA4paA4paR4paI4paI4paI4paE4paA4paE4paI4paI4paR4paI4paI4paR4paI4paI4paR4paI4paI4paI4paI4paICuKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgOKWgA=="
so = base64.b64decode(base64_str3).decode()

epi="\033[91mFor updated versions and information, please visit:\033[0m \033[92mhttps://github.com/poursalavati/SOVAP \033[0m\n\033[91mIf you find SOVAP useful, please kindly cite:\033[0m\033[92m DOI.org/10.5281/zenodo.7700081\033[0m\n\033[91mFor questions and bugs please contact:\033[0m \033[92mAbdonaser.Poursalavati@agr.gc.ca\033[0m"


base64_str2 = "4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGACuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKivuKjv+KhhuKhgOKhgOKhgOKhgOKisOKjtuKhhuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgArioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDio6DioYTioIjio7/ioYHioYDioLjioZ/ioYDiorjioZ/ioIHiooDioYDioYDioYDioYDioYDioYDioYDiorjio7/ioYDioYDioYDioYDioYDioYDioYAK4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qKg4qO/4qO/4qGA4qGA4qKI4qOj4qOk4qG/4qC34qC/4qC/4qC/4qC24qC+4qKm4qOE4qO84qCB4qGA4qGA4qGA4qGA4qGA4qGA4qK44qO/4qGA4qGA4qGA4qGA4qGA4qGA4qGACuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKjgOKgiOKgmeKjt+KjtuKgn+Kgi+KhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKgieKggeKhgOKhgOKhgOKhgOKhgOKhgOKiuOKjv+KhgOKhgOKhgOKhgOKhgOKhgOKhgArioYDioYDioYDio6Dio6TioYDioIjioJviorPio77ioJ/ioIHiorjio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioYfioYDioYDioYDioYDioYDioYDiorjio7/ioYDioYDioYDioYDioYDioYDioYAK4qGA4qGA4qGA4qC74qC/4qC34qOk4qOk4qG/4qCB4qGA4qGA4qK44qO/4qO/4qO/4qGf4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCb4qCD4qGA4qGA4qGA4qGA4qGA4qGA4qC44qC/4qC24qC24qC24qC24qCG4qGA4qGACuKhgOKhgOKhgOKhgOKjpOKjhOKjoOKjv+KggeKhgOKhgOKhgOKiuOKjv+Kjv+Kjv+Khh+KhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKjoOKjpOKjpOKjpOKhgOKhgOKhgOKhgArioYDioYDiooDio4DioInioIHiorjioYfioYDioYDioYDioYDiorjio7/io7/io7/io7fio7bio7bio7bio7bio7bio7bio7bioYDioYDioYDioYDioYDioYDioYDioYDioYDioInioIHioYDioonio7/ioYbioYDioYAK4qGA4qGA4qK/4qO/4qC34qC24qK/4qGH4qGA4qGA4qGA4qGA4qK44qO/4qO/4qO/4qG/4qC/4qC/4qC/4qC/4qC/4qC/4qC/4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qKg4qG+4qCb4qCL4qCJ4qO/4qGH4qGA4qGACuKhgOKhgOKhgOKhgOKjoOKjpOKivOKjt+KhgOKhgOKhgOKhgOKiuOKjv+Kjv+Kjv+Khh+KhgOKhgOKhgOKhgOKjtuKhgOKjtuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKiu+Kjp+KjgOKjgOKjoOKjv+Khh+KhgOKhgArioYDioYDioYDioYDioInioIHioYDiorvio6bioYDioYDioYDiorjio7/io7/io7/ioYfioLrio5vio7/ioYDio7/ioYDio7/ioYDioYDioYDioYDioYDioYDioYDioYDioYDioInioInioInioIHioInioIHioYDioYAK4qGA4qGA4qGA4qKg4qO24qO24qG24qCb4qC74qOn4qGA4qGA4qK44qO/4qO/4qO/4qGH4qO/4qOp4qO/4qGA4qO/4qGA4qO/4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qK44qGH4qGA4qGA4qGA4qGA4qGA4qGA4qGACuKhgOKhgOKhgOKgiOKgm+Kgi+KhgOKjpOKhnuKgmeKiv+KjpuKjjOKgieKgieKgieKggeKgiOKggeKgiOKhgOKgieKhgOKgieKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKiuOKjh+KjoOKjtOKjpuKjhOKhgOKhgOKhgArioYDioYDioYDioYDioYDioYDioYDioIniooDio6Diob7ioIvioLviob/io7bio7bio6Tio6Tio4Tio4Dio6Dio6Tio6Tio7bioJbioYDioYDioYDioYDioYDioYDioYDiorjioY/ioIHioYDioYDiorvio4fioYDioYAK4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qGA4qO/4qO/4qCB4qKg4qO+4qGA4qGA4qKI4qG/4qCJ4qK/4qCJ4qCZ4qO/4qGA4qCI4qOm4qGE4qGA4qGA4qGA4qGA4qGA4qGA4qK44qGH4qGA4qGA4qGA4qK44qG/4qGA4qGACuKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKioOKjvuKhh+KhgOKgv+KghuKhgOKjv+Kjp+KhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKhgOKiuOKjp+KjhOKjgOKjpOKhv+Kgg+KhgOKhgArioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioIjioJvioIPioYDioYDioYDioYDioJvioJvioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioYDioIjioInioIHioYDioYDioYDioYAKCiA="

lo_str = base64.b64decode(base64_str2).decode()

# Define command line arguments and help menu
parser = argparse.ArgumentParser(description="Batch mode setup to run SOVAP Pipeline",formatter_class=argparse.RawTextHelpFormatter, epilog=epi)
parser.add_argument("-i", "--input-dir", metavar="", help="Input directory containing paired end fastq files (default: current directory)", default=".")
parser.add_argument("-o", "--output-dir", metavar="", help="Output directory to save results (default: same as input directory)")
parser.add_argument("-t", "--threads", metavar="", help="Number of threads to use for external script (default: 16)", type=int, default=16)
parser.add_argument("-x", "--centrifuge-db", metavar="", help="Path to the Centrifuge database")
parser.add_argument("-g", "--genomad-db", metavar="", help="Path to the geNomad database")
parser.add_argument("-d", "--diamond-db", metavar="", help="Path to the Diamond database")
parser.add_argument("-md", "--megan_db", metavar="", help="Path to the Megan database")
parser.add_argument("--megan", help="Run Diamond + Megan (not IMG/VR database)", action="store_true")
parser.add_argument('-v', '--version', action='version', version='\n{}\n{}\n{}'.format(so, HELP_MESSAGE, lo_str), help='Print version, affiliation, and contact information')

if len(sys.argv) == 1:
    print(so)
    print(HELP_MESSAGE)
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

# Get input and output directory paths
input_dir = os.path.abspath(args.input_dir)
if not os.path.exists(input_dir):
    print("Error: input directory {} does not exist".format(input_dir))
    sys.exit(1)
if args.output_dir is not None:
    output_dir = os.path.abspath(args.output_dir)
else:
    output_dir = input_dir

# Loop through all the paired end fastq files in the input directory
for file in os.listdir(input_dir):
    if file.endswith("_R1_001.fastq.gz"):
        # Extract the sample name from the R1 file name
        sample = file[:-16]

        # Check if the paired end R2 file exists
        r2_file = os.path.join(input_dir, sample + "_R2_001.fastq.gz")
        if not os.path.exists(r2_file):
            print("Error: missing R2 file for sample {}".format(sample))
            continue

        # Create a folder for the sample
        sample_dir = os.path.join(output_dir, sample)
        os.makedirs(sample_dir, exist_ok=True)

        # Run the external script with the R1/R2 file names and other arguments
        cmd = script_cmd.format(
            script_dir,
            script_file,
            os.path.join(input_dir, file),
            r2_file,
            args.threads,
            args.centrifuge_db,
            args.genomad_db,
            args.diamond_db
        )
        if args.megan:
            cmd += " --megan -md {}".format(args.megan_db)
#TO Do: seqkit replace + cat clusters for all folders, then run diamond IMGVR for bunch mode. instead of running in external script.
        #stdout_file = os.path.join(sample_dir, "stdout.txt")
        #stderr_file = os.path.join(sample_dir, "stderr.txt")
        #with open(stdout_file, "w") as out, open(stderr_file, "w") as err:
        #    subprocess.run(cmd, shell=True, cwd=sample_dir, stdout=out, stderr=err)
        print(f'\n\033[33mSrart Processing {sample}...\033[0m\n')
        subprocess.run(cmd, shell=True, cwd=sample_dir)
