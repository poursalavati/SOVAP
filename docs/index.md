  <p align="center">
  <img src="https://user-images.githubusercontent.com/35867448/230953023-dd59a381-5873-4cc4-825b-b35338e370d5.svg" alt="" height="130">
</p>  

# SOVAP v.1.3
## _Soil Virome Analysis Pipeline_
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7700081.svg)](https://doi.org/10.5281/zenodo.7700081)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7697520.svg)](https://doi.org/10.5281/zenodo.7697520)

 - [Description](https://github.com/poursalavati/SOVAP#Description)
 - [Requirements and Dependencies](https://github.com/poursalavati/SOVAP#Requirements-and-Dependencies)
 - [Installation](https://github.com/poursalavati/SOVAP#Installation)
 - [Running the Pipeline - Normal Mode](https://github.com/poursalavati/SOVAP#Running-the-Pipeline---Normal-Mode)
 - [Running the Pipeline - Batch Mode](https://github.com/poursalavati/SOVAP#Running-the-Pipeline---Batch-Mode)
 - [Databases](https://github.com/poursalavati/SOVAP#Databases)
 - [Outputs](https://github.com/poursalavati/SOVAP#Outputs)
 - [Citation](https://github.com/poursalavati/SOVAP#Citation)
 - [Tools citations](https://github.com/poursalavati/SOVAP#Tools-citations)
 

#### Description
The study of viral communities in complex environmental samples, such as **soil**, can provide valuable insights into the diversity and functions of viral communities in the ecosystem. However, processing and analyzing of virome data can be a challenging task that requires the integration of various computational tools and techniques.

To address these challenges, we have developed **SOVAP** pipeline that utilizes a suite of state-of-the-art tools for processing, analysis, and annotation viromics and metagenomics data. 

It utilizes various tools such as **Fastp** and **Centrifuge** for preprocessing and contamination removal, **geNomad**, **Diamond** and **Megan** for identification and annotation of viral contigs which are assembled and clustered using **Megahit** and **CD-HIT**. Additionally, this pipeline provides an **estimate of the abundance** of viral contigs, allowing for a more comprehensive understanding of the virome within the sample. 
The integration of these tools offers a reliable and effective means of taxonomy classification and annotation of viral contigs, aiding researchers in gaining insight into the composition and function of the virome within the analyzed sample.  
<p align="center">
  <img src="https://user-images.githubusercontent.com/35867448/222940533-7fc0776c-4518-48e7-9d81-2d6f7ef92f64.png" alt="" height="500">
</p>  

By integrating the SOVAP pipeline with **IMG/VR** and **geNomad**, it is possible to identify a wider range of viruses, including those that were previously unknown.

The **batch-mode** script allows for the processing of multiple datasets using the SOVAP pipeline. This feature is particularly useful for **large-scale** analyses, such as those involving multiple environmental samples or large sequencing datasets.  
```
The following features are coming soon:
The new approach to analyze using both Diamond Databases simultaneously (Genbank and then IMG/VR)
Add Recentrifuge to analyze centrifuge outputs and visualize them
Add Spades to the assembly step, so user can choose between Spades and Megahit
Add removing specific host reads before Centrifuge (using BBDuk)
```
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
 - [Recentrifuge=1.10.0](http://www.recentrifuge.org/)

## Installation

### Using Conda
First we need to add these channels to the conda config file (if not already added):

Add the required channels:

	conda config --add channels defaults
	conda config --add channels bioconda
	conda config --add channels conda-forge

Then the easiest way to install the required tools and libraries is using conda yaml files to create seperate environments:

Clone the repository:
	
```
git clone https://github.com/poursalavati/SOVAP.git
  
cd SOVAP
```


    conda env create -f centrifuge.yml
    conda env create -f megan.yml
    conda env create -f genomad.yml
    conda env create -f SOVAP.yml
    
or using conda install command:

    conda create -n centrifuge centrifuge=1.0.4 recentrifuge=1.10.0
    conda create -n megan megan
    conda create -n genomad genomad
    conda create -n SOVAP python=3.8 seqkit samtools=1.15.1 fastp=0.23.2 megahit bwa=0.7.17 diamond cd-hit=4.8.1


### Using Docker and Singularity
	This section will be added soon

## Running the Pipeline - Normal Mode

To run the SOVAP pipeline, you can use the `Run_SOVAP.py` provided. 
Here are the steps to run the pipeline:

1.  Activate the Conda environment:  
The order of activating the environments is important and prevents errors in pipeline execution.  

```
conda activate centrifuge
conda activate --stack megan
conda activate --stack genomad
conda activate --stack SOVAP
```
	
2.  Run the SOVAP pipeline in normal mode:

```
python ./Run_SOVAP.py
```

Example command - 1 (IMG/VR database):

```
python ./Run_SOVAP.py -r1 Virome_R1_001.fastq.gz -r2 Virome_R2_001.fastq.gz -t 25 -x centrifuge/p_compressed/p_compressed -g genomad_db/ -d Diamond/IMGVR.dmnd --end_to_end
```

Example command - 2 (NCBI database + DIAMOND-MEGAN):

```
python ./Run_SOVAP.py -r1 Virome_R1_001.fastq.gz -r2 Virome_R2_001.fastq.gz -t 25 -x centrifuge/p_compressed/p_compressed -g genomad_db/ -d Diamond/DIAMOND_viral_database_GB.dmnd -md megan-map/megan-map-Feb2022.db --megan --end_to_end
```  
<p align="center">
  <img src="https://user-images.githubusercontent.com/35867448/222979484-e5838152-c2b0-4895-b55c-14afcc99a2e6.png" alt="" height="500">
</p>   

## Running the Pipeline - Batch Mode

Batch mode in SOVAP allows for efficient analysis of large datasets by running the pipeline on multiple paired-end fastq files. 
The user can provide a directory containing all the files to be processed. The pipeline will automatically loop through all files and run the selected options for each dataset, saving the results in separate output directories.

To run the SOVAP pipeline in batch mode you can use the `SOVAP_BatchMode.py`.   

> Note: To run in batch mode, both scripts should be in the same directory

```
python ./SOVAP_BatchMode.py
```

Example command - 1 (IMG/VR database - Assuming that the current folder contains multiple paired-end fastq files):

```
python ./SOVAP_BatchMode.py -i . -o .  -t 25 -x centrifuge/p_compressed/p_compressed -g genomad_db/ -d Diamond/IMGVR.dmnd --end_to_end
```


Example command - 2 (NCBI database + DIAMOND-MEGAN - Assuming that the current folder contains multiple paired-end fastq files):

```
python ./SOVAP_BatchMode.py -i . -o . -t 25 -x centrifuge/p_compressed/p_compressed -g genomad_db/ -d Diamond/DIAMOND_viral_database_GB.dmnd -md megan-map/megan-map-Feb2022.db --megan --end_to_end
```  
<p align="center">
  <img src="https://user-images.githubusercontent.com/35867448/222979327-5fa10861-3491-482c-99f5-27f718ce4c22.png" alt= “” height="450">
</p>
  

## Databases

### IMG/VR 
To prepare the IMG/VR database for use with the Diamond analysis step in SOVAP, follow these steps:

1.  Download the latest IMG/VR database (version 4) from the official website ([https://img.jgi.doe.gov/vr/](https://img.jgi.doe.gov/vr/)).
    
2.  Extract the database files to a directory.
    
3.  Use the Diamond software to build a Diamond database from the IMG/VR FASTA files. This can be done using the following command:

```
diamond makedb --in /path/to/imgvr/fasta/files --db /path/to/output/database --threads 32
```

1.  This command will create a new Diamond database file in the specified output directory using the IMG/VR FASTA files as input. You can adjust the number of threads used by specifying a different value after `--threads`.
    
2.  Once the Diamond database is built, you can use it with SOVAP by specifying the path to the database file in the `-d , --diamond_db` argument when running the pipeline.
    
Note: Due to the size of the IMG/VR database, building the Diamond database may take several hours or more. It is recommended to use a computer with high processing power and memory for this step (final db size will be more than 65 GB).

While users have the option to use a Genbank virus database, it is strongly recommended to use the IMG/VR database for the best results. The IMG/VR database is a comprehensive and regularly updated database of curated viral genomes that covers a wide range of viral diversity.

### Centrifuge 

The Centrifuge database is a **pre-indexed database** that contains a comprehensive collection of bacterial and archaeal reference genomes. The pipeline uses this database to classify reads to bacterial taxa as well as to subtract bacterial contamination from metagenomic datasets. The database is indexed to enable fast and accurate classification of the reads, and it can handle large datasets efficiently. The use of this database ensures that the pipeline accurately identifies bacterial contaminants and removes them from the datasets, thereby improving the accuracy of **downstream analysis**. Overall, the use of the Centrifuge database is an essential step in the SOVAP pipeline for the analysis of metagenomic datasets.

This is a compressed database built from RefSeq genomes of **Bacteria and Archaea**. The following commands will download and extract centrifuge database:

    mkdir centrifuge
    wget https://genome-idx.s3.amazonaws.com/centrifuge/p_compressed_2018_4_15.tar.gz
    tar -xzvf p_compressed_2018_4_15.tar.gz -C centrifuge
    rm p_compressed_2018_4_15.tar.gz

### Megan and NCBI Viral database
The Megan database is optional and only needed if the user decides to use the `--megan` flag for the pipeline. 
The `--megan` flag will run the DIAMOND analysis and _DAA_-_Meganizer_ step and will require both the NCBI virus database (in diamond format) and the Megan database.

To download **Megan** database (*megan-map-Feb2022.db.zip*) use its official website:
>https://software-ab.cs.uni-tuebingen.de/download/megan6/welcome.html  

To run Diamond + Megan analysis You can download **our pre-indexed** Genbank database here:  

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7697520.svg)](https://doi.org/10.5281/zenodo.7697520)


## Outputs
The outputs of SOVAP pipeline are saved in several subdirectories, each containing the output files generated by a specific step of the pipeline. The subdirectories are as follows:

**0_Logs**: Contains log files generated during the execution of the pipeline for each step.  

**1_Fastp_Report**: Contains a report with statistics about the quality control performed by Fastp.  

**1_Fastp_Output**: Contains a trimmed version of the input fastq files generated by Fastp.  

**2_Centrifuge_Output**: Contains the output of Centrifuge classification for bacterial reads, used for filtering and analysis of bacterial contamination.  

**2_Clean_Reads**: Contains a cleaned and trimmed version of the input fastq files generated by SOVAP after bacterial contamination filtering.  

**3_Megahit_Output**: Contains the contigs generated by Megahit assembly of non-bacterial reads.  

**4_geNomad_Output**: Contains the annotation output generated by geNomad.  

**5_Clusters_Abundance**: contains the clusters of viral contigs that were generated using CD-HIT and the estimated abundance of each cluster.  

**6_Diamond-Taxonomy**: Contains the output of Diamond classification for viral reads.  

* If using `--megan` flag:  

    **6_Diamond_Megan**: Contains the DAA file generated by Diamond and Meganizer step used for visualization and analysis of viral classification with Megan.  


Here is a tree diagram that shows the directory structure of the "outputs" directory:  

    ├── 0_Logs
    ├── 1_Fastp_Report
    ├── 1_Fastp_Output
    ├── 2_Centrifuge_Output
    ├── 2_Clean_Reads
    ├── 3_Megahit_Output
    ├── 4_geNomad_Output
    ├── 5_Clusters_Abundance
    ├── 6_Diamond-Taxonomy
    ├── * 6_Diamond_Megan
    

## Citation
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7700081.svg)](https://doi.org/10.5281/zenodo.7700081)

>Poursalavati A. (2023). SOVAP v.1.3 : Soil Virome Analysis Pipeline (1.3). Zenodo. https://doi.org/10.5281/zenodo.7700081

### Export
[BibTeX](https://zenodo.org/record/7700081/export/hx) , [CSL](https://zenodo.org/record/7700081/export/csl) , [DataCite](https://zenodo.org/record/7700081/export/dcite4) , [Dublin Core](https://zenodo.org/record/7700081/export/xd) , [DCAT](https://zenodo.org/record/7700081/export/dcat) , [JSON](https://zenodo.org/record/7700081/export/json) , [JSON-LD](https://zenodo.org/record/7700081/export/schemaorg_jsonld) , [GeoJSON](https://zenodo.org/record/7700081/export/geojson) , [MARCXML](https://zenodo.org/record/7700081/export/xm) , [Mendeley](https://www.mendeley.com/import/?url=https://zenodo.org/record/7700081)

## Tools citations

|Tools|Web|Cite
|--|--|--|
|geNomad and IMG/VR 4|[Link](https://github.com/apcamargo/genomad)  |[Paper](https://doi.org/10.1093/nar/gkac1037)
|DIAMOND|[Link](https://github.com/bbuchfink/diamond)  |[Paper](https://doi.org/10.1038/nmeth.3176)
|MEGAN|[Link](http://megan.informatik.uni-tuebingen.de/)  |[Paper](https://doi.org/10.1186/s13062-018-0208-7)
|Centrifuge|[Link](https://ccb.jhu.edu/software/centrifuge/)  |[Paper](https://doi.org/10.1101/gr.210641.116)
|Recentrifuge|[Link](http://www.recentrifuge.org/)  |[Paper](https://doi.org/10.1371/journal.pcbi.1006967)
|DIAMOND-MEGAN|[Link](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/megan6/)  |[Paper](https://doi.org/10.1002/cpz1.59)
|Fastp|[Link](https://github.com/OpenGene/fastp)  |[Paper](https://doi.org/10.1093/bioinformatics/bty560)
|Megahit|[Link](https://github.com/voutcn/megahit)  |[Paper](https://doi.org/10.1093/bioinformatics/btv033)
|BWA-mem|[Link](https://github.com/lh3/bwa)  |[Paper](https://doi.org/10.48550/arXiv.1303.3997)
|CD-HIT|[Link](http://cd-hit.org/)  |[Paper](https://doi.org/10.1093/bioinformatics/bts565)
|Seqkit|[Link](https://bioinf.shenwei.me/seqkit/)  |[Paper](https://doi.org/10.1371/journal.pone.0163962)
|Samtools|[Link](http://www.htslib.org/)  |[Paper](https://doi.org/10.1371/journal.pone.0163962)|
