from mpi4py import MPI
from math import ceil
import sys
import os
import re
import io


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

path = sys.argv[1]
word = sys.argv[2]
show = False if len(sys.argv) <= 3 else True

filelist = []
chunks = []


if rank == 0:
    for (dirpath, dirnames, filenames) in os.walk(path):
        for f in filenames:
            filelist.append(dirpath + '/' + f)

    l = int(ceil(len(filelist) / size))
    chunks = [filelist[i * l: (i+1) * l] for i in range(size)]

todo = comm.scatter(chunks)

print("Process %d got %6d files" % (rank, len(todo)))

count = 0
for name in todo:
    try:
        with io.open(name, mode="r", encoding="utf-8") as f:
            for line in f:
                for w in line.split():
                    if word.lower() == w.lower():
                        if show: print(name, ": ", line)
                        count += 1
    except Exception as e:
        pass

# print("Process %d found %4d occurrences of the word: %s" % (rank, count, word))

final_count = comm.gather(count)

if rank == 0:
    print("Found a total of %d occurrences of the word: %s" % (sum(final_count), word))
