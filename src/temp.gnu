#!/usr/bin/gnuplot

set terminal pngcairo size 1000, 2000 enhanced dashed font 'Verdana,10'
set output "temp_5.png"

set multiplot layout 5, 1 title "Convergence" font ",14"

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

#set title 'Convergence'

set ylabel 'Function Avaliations'

set xlabel 'Score0'
plot 'convergence_stage1__1rop_0005__2017_10_25__14_05_36__7VF8XD.dat' u 1:3 w l notitle ls 1

set xlabel 'Score1'
plot 'convergence_stage2__1rop_0005__2017_10_25__14_05_36__7VF8XD.dat' u 1:3 w l notitle ls 2

set xlabel 'Score2, Score5'
plot 'convergence_stage3__1rop_0005__2017_10_25__14_05_36__7VF8XD.dat' u 1:3 w l notitle ls 3

set xlabel 'Score3'
plot 'convergence_stage4__1rop_0005__2017_10_25__14_05_36__7VF8XD.dat' u 1:3 w l notitle ls 4

set xlabel 'Score3'
plot 'convergence_stage5__1rop_0005__2017_10_25__14_05_36__7VF8XD.dat' u 1:3 w l notitle ls 5
