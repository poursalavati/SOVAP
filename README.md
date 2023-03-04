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

To run the SOVAP pipeline in batch mode and for multiple datasets you can use the `SOVAP_BatchMode.py`.   
> Note: To run in batch mode, both scripts should be in the same directory


    `python SOVAP_BatchMode.py`
    

<img src="https://user-images.githubusercontent.com/35867448/222864393-0461ba16-1cfc-41f9-bb76-dbc234f5a964.png" alt= “” height="400">
