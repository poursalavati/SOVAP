# SOVAP v.1.3
## _Soil Virome Analysis Pipeline_

#### Description
The study of viral communities in complex environmental samples, such as **soil**, can provide valuable insights into the diversity and functions of viral communities in the ecosystem. However, processing and analyzing of virome data can be a challenging task that requires the integration of various computational tools and techniques.

To address these challenges, we have developed **SOVAP** pipeline that utilizes a suite of state-of-the-art tools for processing, analysis, and annotation viromics and metagenomics data. 

It utilizes various tools such as **Fastp** and **Centrifuge** for preprocessing and contamination removal, **geNomad**, **Diamond** and **Megan** for identification and annotation of viral contigs which are assembled and clustered using **Megahit** and **CD-HIT**. Additionally, this pipeline provides an **estimate of the abundance** of viral contigs, allowing for a more comprehensive understanding of the virome within the sample. 
The integration of these tools offers a reliable and effective means of taxonomy classification and annotation of viral contigs, aiding researchers in gaining insight into the composition and function of the virome within the analyzed sample.

By integrating the SOVAP pipeline with **IMG/VR** and **geNomad**, it is possible to identify a wider range of viruses, including those that were previously unknown.

The **batch-mode** script allows for the processing of multiple datasets using the SOVAP pipeline. This feature is particularly useful for **large-scale** analyses, such as those involving multiple environmental samples or large sequencing datasets.

## Requirements and Dependencies
To successfully run the SOVAP pipeline, your system must have the necessary software installed and accessible through the system's path:

  - [Python=3.8](https://www.python.org/downloads/)
 - [geNomad](https://github.com/apcamargo/genomad)
 - [DIAMOND](https://github.com/bbuchfink/diamond)
 - [MEGAN](http://megan.informatik.uni-tuebingen.de/)
 - [Seqkit](https://bioinf.shenwei.me/seqkit/)
 - [Samtools=1.15.1](http://www.htslib.org/)
 - [Fastp=0.23.2](https://github.com/OpenGene/fastp)
 - [Megahit](https://github.com/voutcn/megahit)
 - [bwa=0.7.17](https://github.com/lh3/bwa) 
 - [CD-HIT=4.8.1](http://cd-hit.org/)
 - [Centrifuge=1.0.4](https://ccb.jhu.edu/software/centrifuge/)

## Installation

### Using Conda
First we need to add these channels to the conda config file (if not already added):

Add the required channels:

	conda config --add channels defaults
	conda config --add channels bioconda
	conda config --add channels conda-forge

Then the easiest way to install the required tools and libraries is using conda yaml files to create seperate environments:

    conda env create -f centrifuge.yml
    conda env create -f megan.yml
    conda env create -f genomad.yml
    conda env create -f SOVAP.yml
    
or using conda install command:

    conda create -n centrifuge centrifuge=1.0.4
    conda create -n megan megan
    conda create -n genomad genomad
    conda create -n SOVAP python=3.8 seqkit samtools=1.15.1 fastp=0.23.2 megahit bwa=0.7.17 diamond cd-hit=4.8.1


### Using Docker and Singularity
	This section will be added soon

## Running the Pipeline - Normal Mode

To run the SOVAP pipeline, you can use the `Run_SOVAP.py` provided. 
Here are the steps to run the pipeline:

1.  Clone the repository:
	
```
git clone https://github.com/poursalavati/SOVAP.git`
  
cd SOVAP
```
	
2.  Activate the Conda environment:  
The order of activating the environments is important and prevents errors in pipeline execution.  

```
conda activate centrifuge
conda activate --stack megan
conda activate --stack genomad
conda activate --stack SOVAP
```
	
3.  Run the SOVAP pipeline in normal mode:


    `python Run_SOVAP.py`


<img src="https://user-images.githubusercontent.com/35867448/222854685-148ee0fc-b8c5-4792-a58e-f51d46ed5fc3.png" alt= “” height="500">


## Running the Pipeline - Batch Mode

Batch mode in SOVAP allows for efficient analysis of large datasets by running the pipeline on multiple paired-end fastq files. 
The user can provide a directory containing all the files to be processed. The pipeline will automatically loop through all files and run the selected options for each dataset, saving the results in separate output directories.

To run the SOVAP pipeline in batch mode you can use the `SOVAP_BatchMode.py`.   

> Note: To run in batch mode, both scripts should be in the same directory


    `python SOVAP_BatchMode.py`
    

<img src="https://user-images.githubusercontent.com/35867448/222864393-0461ba16-1cfc-41f9-bb76-dbc234f5a964.png" alt= “” height="400">


## Databases

### IMG/VR 
To prepare the IMG/VR database for use with the Diamond analysis step in SOVAP, follow these steps:

1.  Download the latest IMG/VR database (version 4) from the official website ([https://img.jgi.doe.gov/vr/](https://img.jgi.doe.gov/vr/)).
    
2.  Extract the database files to a directory.
    
3.  Use the Diamond software to build a Diamond database from the IMG/VR FASTA files. This can be done using the following command:

`diamond makedb --in /path/to/imgvr/fasta/files --db /path/to/output/database --threads 32`

1.  This command will create a new Diamond database file in the specified output directory using the IMG/VR FASTA files as input. You can adjust the number of threads used by specifying a different value after `--threads`.
    
2.  Once the Diamond database is built, you can use it with SOVAP by specifying the path to the database file in the `-d , --diamond_db` argument when running the pipeline.
    
Note: Due to the size of the IMG/VR database, building the Diamond database may take several hours or more. It is recommended to use a computer with high processing power and memory for this step (final db size will be more than 65 GB).

While users have the option to use a Genbank virus database, it is strongly recommended to use the IMG/VR database for the best results. The IMG/VR database is a comprehensive and regularly updated database of curated viral genomes that covers a wide range of viral diversity.

### Centrifuge 

For the bacterial database, the pipeline uses the Centrifuge database, which contains pre-indexed  Bacteria and Archaea and is used for the classification of reads to bacterial taxa as well as the subtraction of bacterial contamination.

This is a compressed database built from RefSeq genomes of Bacteria and Archaea. The following commands will download the database:

    mkdir centrifuge
    wget https://genome-idx.s3.amazonaws.com/centrifuge/p_compressed_2018_4_15.tar.gz
    tar -xzvf p_compressed_2018_4_15.tar.gz -C centrifuge
    rm p_compressed_2018_4_15.tar.gz

### Megan and NCBI Viral database
The Megan database is optional and only needed if the user decides to use the `--megan` flag for the pipeline. 
The `--megan` flag will run the DIAMOND analysis and _DAA_-_Meganizer_ step and will require both the NCBI virus database (in diamond format) and the Megan database.

To download Megan database (megan-map-Feb2022.db.zip) use its official website:
https://software-ab.cs.uni-tuebingen.de/download/megan6/welcome.html  

To run Diamond + Megan analysis You can download our pre-indexed Genbank database from here: 
https://zenodo.org/record/7697520

## Outputs

## Tools citations

## Citation
