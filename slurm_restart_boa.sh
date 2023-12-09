#!/bin/bash
#SBATCH --job-name=boa_run
#SBATCH --time=48:00:00
#SBATCH --nodes=1 --ntasks-per-node=28
#SBATCH --output=boa_logs/%j.log
#SBATCH --account=PAS0409

set -x

scheduler_path=$1

echo 'starting optimization'

python -m boa -sp $scheduler_path

echo 'completed optimization'`

time=`date +%FT%H%M%S`
mv ./boa_logs/$SLURM_JOB_ID.log ./boa_logs/${time}_jobid${SLURM_JOB_ID}.log