#!/bin/bash
#SBATCH --job-name=swat_job
#SBATCH --nodes=1 --ntasks-per-node=1
#SBATCH --output=swat_slurm_logs/%j.log
#SBATCH --account=PAS0409

set -x  # for displaying the commands in the log for debugging

trial_dir=$1

echo trial dir here: $trial_dir

Rscript run_model.R $trial_dir

if [ $? -ne 0 ]
then
    echo "Error Finished running run_model.R for $trial_dir" >&2
    writout_failed_status
fi

function writout_failed_status() {
    echo '{"trial_status": "FAILED"}' > $trial_dir/output.json
    exit 1
}

trap writout_failed_status TERM