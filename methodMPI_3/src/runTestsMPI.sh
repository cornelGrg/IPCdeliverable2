rm ../data/csv/OMPtime.csv
mpirun -np 1 ./matTrans

rm ../data/csv/MPItime.csv

mpirun -np 1 ./matTrans -mpi
mpirun -np 2 ./matTrans -mpi
mpirun -np 4 ./matTrans -mpi
mpirun -np 8 ./matTrans -mpi
mpirun -np 16 ./matTrans -mpi
mpirun -np 32 ./matTrans -mpi
mpirun -np 64 ./matTrans -mpi
