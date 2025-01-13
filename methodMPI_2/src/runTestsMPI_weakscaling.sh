rm ../data/csv/SEQtime.csv
rm ../data/csv/OMPtime.csv
mpirun -np 1 ./matTrans

rm ../data/csv/MPItime.csv

mpirun -np 1 ./matTrans -mpi 7
mpirun -np 4 ./matTrans -mpi 8
mpirun -np 16 ./matTrans -mpi 9
mpirun -np 64 ./matTrans -mpi 10
