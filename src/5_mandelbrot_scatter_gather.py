from mpi4py import MPI
import numpy as np

import matplotlib
from matplotlib import colors
import matplotlib.pyplot as plt


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

img_size = 100 * size

img = np.empty(shape=(img_size, img_size))

xmin, xmax = -2.0 , 1.5
ymin, ymax = -1.25, 1.25


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


intervals = []

if rank == 0:
    diff = xmax - xmin
    dx = diff / size
    intervals = [(i, i * dx + xmin, (i+1) * dx + xmin) for i in range(size)]

data = comm.scatter(intervals, root=0)

xmin_ = data[1]
xmax_ = data[2]

r1 = np.linspace(xmin_, xmax_, img_size / size)
r2 = np.linspace(ymin, ymax, img_size)

partial_img = np.empty(shape=(int(img_size/size), img_size), dtype='i')

for i, x in enumerate(r1):
    for j, y in enumerate(r2):
        partial_img[i, j] = mandelbrot(complex(x, y), 255)

full_img = comm.gather(partial_img, root=0)

if rank == 0:
    img = full_img[0].reshape(int(img_size / size), img_size)

    for i in range(1, len(full_img)):
        img = np.concatenate((img, full_img[i].reshape(int(img_size / size), img_size)))

    save(img, "ya")
