#!/bin/bash -l
# created: jun 2020
# author: urenaj1
#SBATCH -J RunPerception
#SBATCH -o logs/out_%J.txt
#SBATCH -e logs/err_%J.txt
#SBATCH -n 1
#SBATCH -t 1:00:00
#SBATCH --mem-per-cpu=2g

module purge
module load swig
module load anaconda2

srun python $HOME/perception/perception_model.py --sav=$1 --sbv=$2 --nv=$3 --cv=$4 --iterations=$5 --run_name=$6 --folder=$7
