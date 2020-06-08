#!/bin/bash

i=441
for sa in `seq .5 .025 1`
do
    for sb in `seq .5 .025 1`
    do
        python2 perception_model.py --sav=$sa \
                --sb=$sb \
                --nv=.1 \
                --cv=0.0 \
                --taa=.5 \
                --tbb=.5 \
                --nodes=2000 \
                --avgdeg=20 \
                --iterations=1000 \
                --run_name=$i \
                --folder=homophilies
        ((i=i+1))
    done
done
