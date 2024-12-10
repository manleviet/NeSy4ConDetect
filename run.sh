#!/bin/bash
#SBATCH --job-name=Task1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --ntasks=1
#SBATCH --time=24:00:00


PROJ_DIR=$HOME/projects/ConDetect/NeSy4ConDetect
PYTHONPATH=$PYTHONPATH:$PROJ_DIR
export PYTHONPATH

echo $HOME
echo $PROJ_DIR
echo $PYTHONPATH

python3 run.py --task=../data/busybox/655
