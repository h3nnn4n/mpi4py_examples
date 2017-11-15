#!/bin/bash

for i in `seq 1 10 200`
do
    mpiexec -n 5 python3.5 mandelbrot_reloaded.py $i | tee -a log2
done
