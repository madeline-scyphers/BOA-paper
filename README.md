# BOA Examples

In this repository, we provide examples of how to use the BOA package to optimize a number of synthetic functions, in a variety of prograamming languages, with single and multi-objective optimization, with and without constraints, and with and without stopping conditions. We also show a few examples of how to use the BOA package to optimize real environmental models, such as SWAT+ and FETCH3.14. In the SWAT+ example, we provide a configuration file for a variety of levels of parallelization as well as a a configuration file for a high-dimensional optimization problem (nearly 100 dimensions). In the FETCH3.14 example, we provide a configuration file for a multi-objective optimization.


## Requirements

- Synthetic functions
- SWAT+

dependencies are included in the `environment.yml` file. (extra R dependencies are listed in the `environment.yml` file comments that can't be installed with conda)

- FETCH3.14

install  BOA from the environment.yml file and then follow the instructions in fetch3/README.md to install FETCH3.14.


## Run Optimization

```bash
python -m boa -c {any of the configuration files in this directory}
```
