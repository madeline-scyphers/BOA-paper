#!/bin/bash
#SBATCH --job-name=boa_run
#SBATCH --time=72:00:00
#SBATCH --nodes=1 --ntasks-per-node=14
#SBATCH --output=boa_logs/%j.log
#SBATCH --account=PAS0409

set -x

config_path=$1

echo 'starting optimization'

python -m boa --config-path $config_path

echo 'completed optimization'`

time=`date +%FT%H%M%S`
mv ./boa_logs/$SLURM_JOB_ID.log ./boa_logs/${time}_jobid${SLURM_JOB_ID}.log