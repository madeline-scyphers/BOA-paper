#!/bin/bash
#SBATCH --job-name=swat_job
#SBATCH --time=75:00
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --output=swat_slurm_logs/%j.log
#SBATCH --account=PAS0409

set -x  # for displaying the commands in the log for debugging

trial_dir=$1

echo trial dir here: $trial_dir

Rscript run_model.R $trial_dir

echo "Finished running run_model.R"