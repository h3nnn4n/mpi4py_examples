from mpi4py import MPI
from math import sqrt
import random
import numpy as np


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

data = []
chunks = []

l = size * 10

if rank == 0:
    data = [random.randint(0, 10) for _ in range(l)]
    chunks = [data[i*(l // size):(i+1)*(l // size)] for i in range(size)]

block = comm.scatter(chunks)

r = 0
data_ = np.asarray(sum(block))
result_ = np.asarray(r)
comm.Allreduce(data_, result_, op=MPI.SUM)

mean = result_ / l

p_std = 0

for d in block:
    p_std += sqrt((d - mean) ** 2.0)

data_ = np.asarray(p_std, dtype='f')
result_ = np.asarray(r, dtype='f')
comm.Reduce(data_, result_, op=MPI.SUM)

if rank == 0:
    std = result_ / (l - 1)

    print("Avg: %f" % mean)
    print("Std: %f" % std)
