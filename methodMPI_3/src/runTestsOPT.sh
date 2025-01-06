rm -rf ../data/csv/*

#!/bin/bash

#compiler settings
module load gcc91
alias gcc=gcc-9.1.0
alias g++=g++-9.1.0

#compilation
g++-9.1.0 -c support.cpp -o ../build/support.o
g++-9.1.0 -c main.cpp -fopenmp -o ../build/main.o
g++-9.1.0 -c matTransSEQ.cpp -o ../build/matTransSEQ.o
g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 -c matTransOMP.cpp -fopenmp -o ../build/matTransOMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans


echo "Matrix size 2^4: (No Optimization)"
./matTrans 4
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^4: (O1)"
./matTrans 4 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^4: (O1, -march)"
./matTrans 4 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^4: (O2)"
./matTrans 4 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^4: (O2, funroll-loops, -march )"
./matTrans 4 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^5: (No optimizations)"
./matTrans 5
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^5: (O1)"
./matTrans 5 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^5: (O1, -march)"
./matTrans 5 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^5: (O2)"
./matTrans 5 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^5: (O2, funroll-loops, -march )"
./matTrans 5 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^6: (No optimizations)"
./matTrans 6
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^6: (O1)"
./matTrans 6 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^6: (O1, -march)"
./matTrans 6 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^6: (O2)"
./matTrans 6 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^6: (O2, funroll-loops, -march )"
./matTrans 6 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^7: (No optimizations)"
./matTrans 7
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^7: (O1)"
./matTrans 7 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^7: (O1, -march)"
./matTrans 7 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^7: (O2)"
./matTrans 7 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^7: (O2, funroll-loops, -march )"
./matTrans 7 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^8: (No optimizations)"
./matTrans 8
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^8: (O1)"
./matTrans 8 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^8: (O1, -march)"
./matTrans 8 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^8: (O2)"
./matTrans 8 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^8: (O2, funroll-loops, -march )"
./matTrans 8 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^9: (No optimizations)"
./matTrans 9
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^9: (O1)"
./matTrans 9 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^9: (O1, -march)"
./matTrans 9 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^9: (O2)"
./matTrans 9 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^9: (O2, funroll-loops, -march )"
./matTrans 9 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^10: (No optimizations)"
./matTrans 10
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^10: (O1)"
./matTrans 10 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^10: (O1, -march)"
./matTrans 10 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^10: (O2)"
./matTrans 10 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^10: (O2, funroll-loops, -march )"
./matTrans 10 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^11: (No optimizations)"
./matTrans 11
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^11: (O1)"
./matTrans 11 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^11: (O1, -march)"
./matTrans 11 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^11: (O2)"
./matTrans 11 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^11: (O2, funroll-loops, -march )"
./matTrans 11 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo

echo "-----------------------------------------"

g++-9.1.0 -c matTransIMP.cpp -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^12: (No optimizations)"
./matTrans 12
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^12: (O1)"
./matTrans 12 ../data/csv/IMPtime_o1.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O1 -march=native -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^12: (O1, -march)"
./matTrans 12 ../data/csv/IMPtime_o1_march.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^12: (O2)"
./matTrans 12 ../data/csv/IMPtime_o2.csv
echo
echo

g++-9.1.0 -c matTransIMP.cpp -O2 -march=native -funroll-loops -o ../build/matTransIMP.o
g++-9.1.0 ../build/support.o ../build/main.o ../build/matTransSEQ.o ../build/matTransIMP.o ../build/matTransOMP.o -fopenmp -o matTrans
echo "Matrix size 2^12: (O2, funroll-loops, -march )"
./matTrans 12 ../data/csv/IMPtime_o2_funroll_march.csv
echo
echo