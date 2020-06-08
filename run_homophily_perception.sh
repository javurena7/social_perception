#!/bin/bash

i=0
for sv in `seq 0 .025 1`
do
    for cv in `seq 0 .1 1`
    do
        for nv in `seq .1 .1 .5`
        do
            python2 perception_model.py --sav=$sv \
                --sb=$sv \
                --nv=$nv \
                --cv=$cv \
                --taa=.5 \
                --tbb=.5 \
                --nodes=2000 \
                --avgdeg=20 \
                --iterations=1000 \
                --run_name=$i \
                --folder=homophily_perception
            ((i=i+1))
        done
    done
done
