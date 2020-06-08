#!/bin/bash

i=0
for sv in `seq .5 .025 1`
do
    for cv in `seq .5 .025 1`
    do
        python2 perception_model.py --sav=$sv \
                --sb=$sv \
                --nv=.1 \
                --cv=$cv \
                --taa=.5 \
                --tbb=.5 \
                --nodes=2000 \
                --avgdeg=20 \
                --iterations=1000 \
                --run_name=$i \
                --folder=homophily_triadic
        ((i=i+1))
    done
    python2 perception_model.py --sav=$sv \
                --sb=$sv \
                --nv=.1 \
                --cv=0.0 \
                --taa=.5 \
                --tbb=.5 \
                --nodes=2000 \
                --avgdeg=20 \
                --iterations=1000 \
                --run_name=$i \
                --folder=homophily_triadic
    ((i=i+1))
done
