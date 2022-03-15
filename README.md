# Introduction 
The FUTURE repository is the "Fourier Transformation Tool to Unravel Renewable Intermittency in the European Power System of the Future"

We are publishing the code alongside the paper which can be downloaded [here]().

The tool has two main purposes:
1. Re-create the fourier decomposition analysis of renewable and load time-series as discussed in the paper.
2. Perform your own analysis for different countries, RES installation scenarios as well as renewable input time-series.


# Getting Started
1. Software dependencies:
   1. Python >= 3.6
   2. JupyterNotebook
2. Installation process:
   1. `git clone` this repository to your local environment
   2. run `pip install -r requirements.txt` to make sure you have all requirements installed
3. open `main.ipynb` as a Jupyter Notebook

   (the notebook must be opened from the same directory as the repository for all references to function)

# Working with the Analysis Tool
4. Download full PECD dataset.
   
   This repository natively only includes a small sample of the full Pan-European-Climate-Database (PECD). 
If you wish to work with the full PECD dataset, please download it from
   - [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3702418.svg)](https://doi.org/10.5281/zenodo.3702418) for PECD 2019 version (ENTSO-E MAF study)
   - [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5780185.svg)](https://doi.org/10.5281/zenodo.5780185) for PECD 2021 version
5. Create renewable capacity scenarios
   
   In `./data/RES_capacity_scenarios.xlsx` you can find an excel file in which you can set up a custom scenario in a separate sheet based on the given template sheet.
