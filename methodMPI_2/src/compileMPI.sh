#!/bin/bash
#module load mpich...

#compilation
mpicxx -c support.cpp -o ../build/support.o
mpicxx -c main.cpp -fopenmp -o ../build/main.o
mpicxx -c matTransSEQ.cpp -o ../build/matTransSEQ.o
mpicxx -c matTransMPI.cpp -o ../build/matTransMPI.o
mpicxx -c matTransOMP.cpp -fopenmp -o ../build/matTransOMP.o
mpicxx ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransMPI.o ../build/matTransOMP.o -fopenmp -o matTrans
