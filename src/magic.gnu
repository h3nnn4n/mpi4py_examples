#!/usr/bin/gnuplot

set terminal pngcairo size 800, 600 enhanced dashed font 'Verdana,10'
set output "time.png"

set style line 11 lc rgb '#808080' lt 1
set border 3 front ls 11
set tics nomirror

set style line 12 lc rgb'#808080' lt 0 lw 1
set grid back ls 12

set style line 1 lw 2 lt 1 lc rgb '#1B9E77'
set style line 2 lw 2 lt 1 lc rgb '#D95F02'
set style line 3 lw 2 lt 1 lc rgb '#7570B3'
set style line 4 lw 2 lt 1 lc rgb '#E6AB02'
set style line 5 lw 2 lt 1 lc rgb '#666666'
set style line 6 lw 2 lt 1 lc rgb '#A6761D'
set style line 7 lw 2 lt 1 lc rgb '#E7298A'
set style line 8 lw 2 lt 1 lc rgb '#66A61E'

set title 'Time versus Granularity'

set ylabel 'Time'

set xlabel 'Slices'
plot 'log' u 1:2 w l notitle ls 1
