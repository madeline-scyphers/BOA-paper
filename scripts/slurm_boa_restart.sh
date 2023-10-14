#!/bin/bash
#SBATCH --job-name=boa_restart_run
#SBATCH --time=12:00:00
#SBATCH --nodes=1 --ntasks-per-node=28
#SBATCH --output=%j.log
#SBATCH --account=PAS0409

set -x

scheduler_path=$1

echo 'restarting optimization from scheduler'

python -m boa --scheduler-path $scheduler_path

echo 'completed restarted optimization'