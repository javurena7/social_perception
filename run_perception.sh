#!/bin/bash -l
# created: jun 2020
# author: urenaj1
#SBATCH -J RunPerception
#SBATCH -o logs/out_%J.txt
#SBATCH -e logs/err_%J.txt
#SBATCH -n 1
#SBATCH -t 1:00:00
#SBATCH --mem-per-cpu=2g

#module purge
#module load swig
#module load anaconda2

#srun
python2 perception_model.py --sav=$1 --sbv=$2 --nv=$3 --cv=$4 --taa=.5 --tbb=.5 --nodes=2000 --avgdeg=20 --iterations=$5 --run_name=$6 --folder=$7
