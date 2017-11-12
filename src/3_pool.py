from mpi4py import MPI
from math import sqrt
import random


def isPrime(n):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    for i in range(3, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
status = MPI.Status()

block = False


data = list(range(1000000))

if rank == 0:
    acc = 0
    for d in data:
        code, n, result = comm.recv(source=MPI.ANY_SOURCE, status=status)
        if code == 'BOOT':
            pass
        if code == 'OK':
            acc += result

        comm.send(('RUN', d), dest=status.Get_source())

    for i in range(1, size):
        code, n, result = comm.recv(source=MPI.ANY_SOURCE, status=status)
        if code == 'OK':
            acc += result
        comm.send(('DIE', -1), dest=status.Get_source())

    print("Found %d prime numbers" % acc)
    if block: comm.barrier()
else:
    t = 0
    comm.send(('BOOT', -1, -1), dest=0)
    while True:
        code, value = comm.recv(source=0)
        if code == 'DIE':
            break
        else:
            t += 1
            v = 1 if isPrime(value) else 0
            comm.send(('OK', value, v), dest=0)
    if block: comm.barrier()
    print("%2d got %d jobs" % (rank, t))

if block: comm.barrier()
print("Process %d has exited" % rank)
