from mpi4py import MPI


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

ping_limit = 10
pings = 0

while pings < ping_limit:
    if rank == 0:
        pings += 1
        print("MASTER sending ping #%2d" % pings)
        comm.send(pings, dest=1)

        if pings < ping_limit:
            x = comm.recv(source=1)
    else:
        pings = comm.recv(source=0)
        print("SLAVE got ping #%2d" % pings)

        if pings < ping_limit:
            comm.send(pings, dest=0)

print("%2d has exited" % rank)
