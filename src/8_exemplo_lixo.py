from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

data = [i + rank*10 for i in range(size)]

print("%d has: %s" % (rank, data))


comm.barrier()
if rank == 0: print()

data = comm.alltoall(data)

print("%d has: %s" % (rank, data))
