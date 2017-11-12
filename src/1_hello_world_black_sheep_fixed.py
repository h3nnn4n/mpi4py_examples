from mpi4py import MPI
import random


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

black_sheep = random.randint(0, size - 1)
black_sheep = comm.bcast(black_sheep, root=0)

if rank != black_sheep:
    print("Hello from %2d out of %2d" % (size, rank))
else:
    print("Hi, my name is %d. Welcome to Jackass!" % rank)
