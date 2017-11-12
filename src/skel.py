from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
