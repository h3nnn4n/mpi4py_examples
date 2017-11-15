from mpi4py import MPI
import random
import numpy as np
from math import sqrt


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

l = 1200

data = []
recv_buffer = []
chunks = []


if rank == 0:
    data = [random.randint(0, 100) for _ in range(l)]
    chunks = [data[i*(l // size):(i+1)*(l // size)] for i in range(size)]

block = comm.scatter(chunks)
s = sum(block)
sums = comm.gather(s)

mean = None
if rank == 0:
    mean = sum(sums) / l
    print(mean)

mean = comm.bcast(mean)

p_std = 0

for d in block:
    p_std += sqrt((d - mean) ** 2.0)

p_stds = comm.gather(p_std)

if rank == 0:
    std = sum(p_stds) / (l - 1)

    print("Std: %f" % std)
