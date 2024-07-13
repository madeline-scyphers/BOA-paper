# BOA Examples

In this repository, we provide examples of how to use the BOA package to optimize a number of synthetic functions, in a variety of programming languages, with single and multi-objective optimization, with and without constraints, and with and without stopping conditions. We also show a few examples of how to use the BOA package to optimize real environmental models, such as SWAT+ and FETCH3.14. In the SWAT+ example, we provide a configuration file for a variety of levels of parallelization as well as a a configuration file for a high-dimensional optimization problem (nearly 100 dimensions). In the FETCH3.14 example, we provide a configuration file for a multi-objective optimization.


## Requirements

### Synthetic functions alone or MacOS

```{note}
The instrutions below in the `Synthetic functions and SWAT+` do not work on MacOS because of the dependencies needed for the SWAT examples. If you are only running the Synthetic functions and FETCH3.14, just the Synthetic functions, or using MacOS, you can use the `environment_synthethitcs.yml` file inplace of the `environment.yml` file in the instructions below.

```

### Synthetic functions and SWAT+

Synthetic function and SWAT dependencies are included in the `environment.yml` file. 

extra R dependencies are listed in the `environment.yml` file comments that can't be installed with conda, or there is an R script to install those dependencies that can be ran after the conda environment is created and activated.

With the `environment.yml` file, you can create a conda environment with the following command:

#### Create Conda Environment

```bash
conda env create -f environment.yml
```

or with mamba

```bash
mamba env create -f environment.yml
```

#### Activate Conda Environment

Activate the environment with the following command:

```bash
conda activate boa-paper
```

or with mamba

```bash 
mamba activate boa-paper
```

#### Install Extra SWAT+ R Dependencies

After you have activated the environment, to finish install all the SWAT+ dependencies, make sure to install the extra R dependencies with the following command:


```bash
Rscript install_github_r_deps.R
```

if this doesn't work, make sure your conda environment is activated by running `conda activate boa-paper` or `mamba activate boa-paper` and then you can run the `Rscript install_github_r_deps.R` command again, or enter the R console and run the following commands manually (enter `R` in the terminal to enter the R console):

```R
devtools::install_github("chrisschuerz/SWATdata")
devtools::install_github("chrisschuerz/SWATrunR")
```

Exit the R console by typing `q()` and hitting enter.

### FETCH3.14

To install FETCH3.14, follow the instructions in fetch3/README.md to install FETCH3.14.


## Run Optimization

```bash
python -m boa -c {any of the configuration files in this repository}
```
