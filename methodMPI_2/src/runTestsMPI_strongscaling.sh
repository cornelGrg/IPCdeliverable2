rm ../data/csv/OMPtime.csv
mpirun -np 1 ./matTrans

rm ../data/csv/MPItime.csv

mpirun -np 1 ./matTrans -mpi 12
mpirun -np 2 ./matTrans -mpi 12
mpirun -np 4 ./matTrans -mpi 12
mpirun -np 8 ./matTrans -mpi 12
mpirun -np 16 ./matTrans -mpi 12
mpirun -np 32 ./matTrans -mpi 12
mpirun -np 64 ./matTrans -mpi 12
