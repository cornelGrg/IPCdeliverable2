#!/bin/bash

#compiler settings
module load gcc91
alias gcc=gcc-9.1.0
alias g++=g++-9.1.0

#compilation
g++-9.1.0 -c support.cpp -o ../build/support.o
g++-9.1.0 -c main.cpp -fopenmp -o ../build/main.o
g++-9.1.0 -c matTransSEQ.cpp -o ../build/matTransSEQ.o
g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 -c matTransOMP.cpp -fopenmp -o ../build/matTransOMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
