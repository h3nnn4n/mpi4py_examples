from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

print("Hello from %2d out of %2d" % (rank, size))
