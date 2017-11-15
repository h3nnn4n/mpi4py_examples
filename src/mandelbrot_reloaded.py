from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
status = MPI.Status()

block = False
verbose = False
gnuplot = True

img_size = 200 * size

img = np.empty(shape=(img_size, img_size))

xmin, xmax = -2.0 , 1.5
ymin, ymax = -1.25, 1.25

splits = size
if len(sys.argv) > 1:
    splits = int(sys.argv[1])

full_img = [[] for _ in range(splits)]

def mandelbrot(c, maxiter):
    z = c
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return 0


def save(data, name):
    with open(name + ".ppm", "w") as f:
        f.write("P2\n")
        f.write("%d %d\n" % (img_size, img_size))
        f.write("255\n")

        for i in data:
            for j in i:
                f.write("%d " % j)
            f.write("\n")

start = 0
if rank == 0:
    start = MPI.Wtime()
    diff = xmax - xmin
    dx = diff / splits
    intervals = [(i, i * dx + xmin, (i+1) * dx + xmin) for i in range(splits)]

    for d in intervals:
        code, n, result = comm.recv(source=MPI.ANY_SOURCE, status=status)
        if code == 'BOOT':
            pass
        if code == 'OK':
            full_img[n] = result

        comm.send(('RUN', d), dest=status.Get_source())

    for i in range(1, size):
        code, n, result = comm.recv(source=MPI.ANY_SOURCE, status=status)
        if code == 'OK':
            full_img[n] = result
        comm.send(('DIE', -1), dest=status.Get_source())

    if block: comm.barrier()
else:
    t = 0
    time = 0
    comm.send(('BOOT', -1, -1), dest=0)
    while True:
        code, data = comm.recv(source=0)
        if code == 'DIE':
            break
        else:
            t += 1
            xmin_ = data[1]
            xmax_ = data[2]

            r1 = np.linspace(xmin_, xmax_, img_size / splits)
            r2 = np.linspace(ymin, ymax, img_size)

            partial_img = np.empty(shape=(int(img_size/splits), img_size), dtype='i')

            start = MPI.Wtime()

            for i, x in enumerate(r1):
                for j, y in enumerate(r2):
                    partial_img[i, j] = mandelbrot(complex(x, y), 255)

            time += MPI.Wtime() - start

            comm.send(('OK', data[0], partial_img), dest=0)
    if block: comm.barrier()
    if verbose: print("%2d got %d jobs and took %f seconds to complete" % (rank, t, time))

if block: comm.barrier()
if verbose: print("Process %d has exited" % rank)

if rank == 0:
    img = full_img[0].reshape(int(img_size / splits), img_size)

    for i in range(1, len(full_img)):
        img = np.concatenate((img, full_img[i].reshape(int(img_size / splits), img_size)))

    if gnuplot:
        print(splits, MPI.Wtime() - start)
    else:
        save(img, "ya")
