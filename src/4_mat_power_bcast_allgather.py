from mpi4py import MPI
import numpy as np


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

iters = 5

scale = 1

msize = (size - 0) * 3

mat = np.empty((msize, msize), dtype='i')
cols = np.empty((scale, msize), dtype='i')
result = np.empty((msize, msize), dtype='i')

if rank == 0:
    mat = np.random.randint(2, size=(msize, msize), dtype='i')

comm.Bcast(mat, root=0)

if rank != 0 or True:
    itens = [i + (rank - 0) * scale for i in range(scale)]

    for i in range(iters):
        for i, i2 in zip(itens, range(scale)):
            for j in range(0, msize):
                cols[i2, j] = np.inner(mat[i], mat[:, j])

        comm.Allgather(cols, mat)

if rank == 0:
    print(mat)
