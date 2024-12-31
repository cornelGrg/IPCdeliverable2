#!/bin/bash

#compilation
g++-11 -c support.cpp -o ../build/support.o
g++-11 -c main.cpp -fopenmp -o ../build/main.o
g++-11 -c matTransSEQ.cpp -o ../build/matTransSEQ.o
g++-11 -c matTransIMP.cpp -O3 -o ../build/matTransIMP.o
g++-11 -c matTransOMP.cpp -fopenmp -o ../build/matTransOMP.o
g++-11 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
