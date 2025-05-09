#!/bin/bash
#SBATCH --job-name=Task1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --ntasks=1
#SBATCH --time=24:00:00


#PROJ_DIR=$HOME/WORK/projects/ConDetect/NeSy4ConDetect
PROJ_DIR=$HOME/Development/GitHub/NeSy4ConDetect
PYTHONPATH=$PYTHONPATH:$PROJ_DIR
export PYTHONPATH

echo $HOME
echo $PROJ_DIR
echo $PYTHONPATH

#python3 run.py --task=$PROJ_DIR/data/busybox/655 --model=dnn
#python3 run.py --task=$PROJ_DIR/data/busybox/126725 --model=dnn
python3 run.py --task=$PROJ_DIR/data/busybox/655 --kb=$PROJ_DIR/data/busybox/kb/busybox.dimacs  --model=cnl
