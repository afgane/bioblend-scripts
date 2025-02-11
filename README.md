# Benchmarking Scripts
An opinionated Python Bioblend script for automating benchmarking tasks in Galaxy.



## Installation

1. Clone this repository.
   ```bash
   git clone https://github.com/ksuderman/bioblend-scripts.git
   cd bioblend-scripts
   ```
1. Create a virtual env and install the required libraries
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Credentials

You will need an [API key](https://training.galaxyproject.org/training-material/faqs/galaxy/preferences_admin_api_key.html) for every Galaxy instance you would like to intereact with.  The `abm` script loads the Galaxy server URLs and API keys from a Yaml configuration file that it expects to find in `$HOME/.abm/profile.yml`.  You can use the `profile-sample.yml` file as a starting point and it includes the URLs for all Galaxy instances we haves used to date (Sept 22, 2021 as of this writing). 

## Usage

To get general usage information run the command:

```bash
python3 abm help
```

You can get information about a specific `abm` command with:

```bash
python3 abm workflow help
```

When running a command (i.e. not just printing help) you will need to specify the Galaxy instance to target as the first parameter:

```bash
python3 abm aws workflow list
python3 abm aws workflow run configs/paired-dna.yml
```

## Runtime Configuration

The runtime parameters for benchmarking runs are specified in a YAML configuration file.  The configuration file can contain more than one runtime configuration specified as a YAML list. This file can be stored anywhere, but several examples are included in the `config` directory. 

The YAML configuration for a single workflow looks like:

```
- workflow_id: d6d3c2119c4849e4
  output_history_base_name: RNA-seq
  reference_data:
    - name: Reference Transcript (FASTA)
      dataset_id: 50a269b7a99356aa
      runs:
    - history_name: 1
      inputs:
      - name: FASTQ RNA Dataset
        dataset_id: 28fa757e56346a34
    - history_name: 2
      inputs:
      - name: FASTQ RNA Dataset
        dataset_id: 1faa2d3b2ed5c436
```

- **workflow_id** 
  The ID of the workflow to run.
  
- **output_history_ base_name**  (optional)
  Name to use as the basis for histories created.  If the *output_history_base_name* is not specified then the  *workflow_id* is used.
  
- **reference_data** (optional)
  Input data that is the same for all benchmarking runs and only needs to be set once.  See the section on *inputs* below for a description of the fields

- **runs**
  Input definitions for a benchmarking run.  Each run defintion shoud contain:

  - **history_name** (optional) 
    The name of the history created for the output.  The final output history name is generated by concatenating the *output_history_base_name* from above and the *history_name*.  If the *history_name* is not specified an incrementing integer counter is used.
  - **inputs**
    The one or more input datasets to the workflow.  Each input specification consists of:
    1. **name** the input name as specified in the workflow editor
    2. **dataset_id** the History API ID as displayed in the workflow editor or with the  `abm history list` command.

## Moving Workflows

The `workflow translate` and `workflow validate` commands can be used when moving workflows and datasets between Galaxy instances.  The `workflow translate` command takes the path to a workflow configuration file, translates the workflow and dataset ID values to their name as it appears in the Galaxy user interface, and write the configuration to stdout.  To save the translated workflow configuration simple redirect the output to a file

```bash
python3 abm aws workflow translate config/rna-seq.yml > config/rna-seq-named.yml
```

Then use the `workflow validate` command to ensure that the other Galaxy instance has the same workflow and datasets installed.

```b
python3 abm gcp workflow validate config/rna-seq-named.yml
```



## Future Work

- Integrate with the [Galaxy Benchmarker](https://github.com/usegalaxy-eu/GalaxyBenchmarker)
- Use as much as we can from [Git-Gat](https://github.com/hexylena/git-gat)

## Contributing

Fork this repository and then create a working branch for yourself from the `dev` branch. All pull requests should target  `dev` and not the `master` branch.

```bash
git clone https://github.com/ksuderman/bioblend-scripts.git
cd bioblend-scripts
git checkout -b my-branch
```

If you decide to work on one of the [issues](bioblend-scripts/issues) be sure to assign yourself to that issue to let others know the issue is taken.

