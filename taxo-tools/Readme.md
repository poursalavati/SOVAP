# Taxonomy and Abundance Tools for SOVAP Downstream Analysis

This folder contains two scripts designed for post-SOVAP analysis. These tools allow users to retrieve assigned taxonomies (lineage assignment) and merge them with abundance data for downstream analysis.

## Features
- **Single and Batch Modes**: Run the scripts on a single folder or in batch mode for multiple folders.
- **Lineage Retrieval**: Extracts and retrieves lineage information for previously assigned taxonomies.
- **Abundance Merging**: Merges taxonomy data with abundance files to produce comprehensive datasets.
- **Customizable Workflow**: Choose to perform only lineage retrieval, abundance merging, or both.

## Scripts Overview

### 1. **Prompt-based Script**
This script [SOVAP_taxo_merge_prompt.sh] interacts with the user, asking for the folder name, mode (single or batch), and the desired operation (lineage retrieval, merging, or both). It supports tab-autocomplete for file paths, making it easier to navigate and select files. Ideal for users who prefer guided inputs.

### 2. **Flag-based Script**
This script [SOVAP_taxo_merge_auto.sh] accepts command-line arguments and flags, allowing fully automated execution. No prompts are given, and the user must specify all options directly when running the script.

Both scripts are designed to support **lineage assignment** using a sorted `IMGVR_all_Sequence_information.tsv` file and **merging** with abundance data for further downstream analysis.

### Requirements
- The **IMGVR_all_Sequence_information.tsv** file (`seqinfo`) **must be sorted** prior to running the scripts.
- Make sure you have run **SOVAP** and have the necessary output files (taxonomy and abundance) in place.

---

### Script 1: `SOVAP_taxo_merge_prompt.sh`

This script allows interactive selection of:
- **Mode**: Taxonomy-only, merge-only, or both.
- **Operation**: Single-folder or batch mode (processes all folders in the current directory).

#### Features:
- **Interactive Prompts**: The script asks the user whether to run in **single-folder** or **batch** mode.
- **Operation Mode**: You can choose whether to:
  - Run only taxonomy retrieval.
  - Merge taxonomy with abundance data.
  - Perform both operations in sequence.
- **Autocomplete**: This version supports tab autocompletion to help select file paths during input prompts.

During execution, the script will guide you through the following:
1. Selecting **single-folder** or **batch** mode.
2. Choosing whether to:
   - Run taxonomy retrieval only.
   - Merge abundance with taxonomy only.
   - Perform both.
3. If taxonomy is selected, you will be prompted to provide the path to the **sorted** `IMGVR_all_Sequence_information.tsv` file.

### Example Workflow:
```bash
./SOVAP_taxo_merge_prompt.sh
```
This command will prompt you to select the mode and provide necessary file paths.

---

### Script 2: `SOVAP_taxo_merge_auto.sh`

This version is more suited for automated workflows where no user interaction is required. It uses command-line flags and arguments to specify the mode and input files.

#### Features:
- **No Interactive Prompts**: All inputs are passed via command-line arguments.
- **Modes**: Taxonomy-only, merge-only, or both.
- **Batch Mode**: You can process all folders in the current directory at once using the `--batch` flag.

#### Usage:

To see detailed help:
```bash
./SOVAP_taxo_merge_auto.sh --help
```

#### Available Flags:
- `--batch`: Process all folders in the current directory.
- `--seqinfo <file>`: Provide the path to the **sorted** `IMGVR_all_Sequence_information.tsv` file (required for taxonomy retrieval).
- `--taxonomy-only`: Perform only taxonomy retrieval.
- `--merge-only`: Perform only merging of abundance with taxonomy.
- `--both`: Run both taxonomy retrieval and merging.
- `<folder_name>`: If not in batch mode, provide the folder name to process.

#### Example Workflows:

1. **Single Folder, Taxonomy Only**:
   ```bash
   ./SOVAP_taxo_merge_auto.sh --taxonomy-only --seqinfo /path/to/sorted_IMGVR_all_Sequence_information.tsv <folder_name>
   ```

2. **Batch Mode, Both Taxonomy Retrieval and Merging**:
   ```bash
   ./SOVAP_taxo_merge_auto.sh --batch --both --seqinfo /path/to/sorted_IMGVR_all_Sequence_information.tsv
   ```

3. **Help**:
   ```bash
   ./SOVAP_taxo_merge_auto.sh --help
   ```

#### Key Points:
- The **`--seqinfo` argument** is required for taxonomy retrieval.
- The script will automatically detect `.tsv` files in the relevant directories for both **taxonomy** and **abundance** processing.  

---

### Workflow Overview:

After completing **SOVAP** analysis:
1. Run one of these scripts to:
   - Retrieve taxonomies to the contigs based on a sorted `IMGVR_all_Sequence_information.tsv` file.
   - Merge taxonomy information with abundance data for further downstream analysis.
2. Use the output files for your subsequent analyses, such as diversity metrics, visualizations, or comparative studies.

---

These tools provide flexibility for users who prefer either **interactive** or **non-interactive** processing and are specifically tailored for use after **SOVAP** has been run.

