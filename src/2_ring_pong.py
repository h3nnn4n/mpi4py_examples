from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

token = 0

if rank != 0:
    token = comm.recv(source=rank - 1)
    print("%2d sending to %2d" % (rank, (rank+1) % size))
    comm.send(token, dest=(rank + 1) % size)

if rank == 0:
    print("%2d sending to %2d" % (rank, (rank+1) % size))
    comm.send(token, dest=(rank+1) % size)
    comm.recv(source=size - 1)
