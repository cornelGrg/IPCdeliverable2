# IPCdeliverable2
![Author](https://img.shields.io/badge/Author-Cornel%20Grigor%20235986-informational)
![Language](https://img.shields.io/badge/C++-8A2BE2)
![Language](https://img.shields.io/badge/Python-green)
![Language](https://img.shields.io/badge/HPC-red)
![Language](https://img.shields.io/badge/MPI-cyan)
![Language](https://img.shields.io/badge/OpenMP-yellow)

Repository created for the second deliverable of the "Introduction to Parallel Computing" course at University of Trento, A.A 24/25.

## Git Repository:
https://github.com/cornelGrg/IPCdeliverable2

## Assignment
The assignment consists of benchmarking and studying the effects of different parallelization techniques used to optimize a squared matrix transposition, the second part focuses on MPI. The whole report can be found by opening the __report.pdf__ file.

## Reproducibility
All the tests were done using the University's cluster with _MPICH version 3.2.1 based on GCC 9.1.0_.

The main project is written in C++ while the plotter program is written in Python.

Start by downloading the repository, where you can find multiple *methodMPI_X* folders, each folder contains a different approach that was tested during the making of the report, every algorithm has the same exact folder structure and the instructions below apply to all of them.

- methodMPI_1: Naive Out-of-Place per row divided and gather approach
- methodMPI_2: Naive Out-of-Place scatter local transpose with gather on shared memory
- methodMPI_3: Naive Out-of-Place scatter local transpose with final reduction

For the best performance overall and the actual method deemed succesfull run *methodMPI_1*. 
You can find already generated graphs for methodMPI_1 inside the graph folder `/methodMPI_1/data/graphs/` to see the performance analyzed in the report.

### Directory structure
```bash
IPCdeliverable2/
├── csv_backups
├── methodMPI_1 #Naive per row divided and gather approach
│   ├── build
│   ├── data
│   │   ├── csv
│   │   │   ├── csv_strongscaling
│   │   │   └── csv_weakscaling
│   │   └── graphs
│   ├── include
│   ├── python
│   └── src
├── methodMPI_2 #Naive scatter local transpose with gather on shared memory
│   ├── build
│   ├── data
│   │   ├── csv
│   │   │   ├── csv_strongscaling
│   │   │   └── csv_weakscaling
│   │   └── graphs
│   ├── include
│   ├── python
│   └── src
├── methodMPI_3 #Naive scatter local transpose with final reduction
│   ├── build
│   ├── data
│   │   ├── csv
│   │   │   ├── csv_strongscaling
│   │   │   └── csv_weakscaling
│   │   └── graphs
│   ├── include
│   ├── python
│   └── src
└── pbsOutputs
```

### Testing instructions
(These instructions apply to all the 3 methods)
There are two ways to run the program inside the cluster:
Before doing everything clone the repository using `git clone https://github.com/cornelGrg/IPCdeliverable2`

In case you download the zip manually from github.com please rename the folder project from `IPCdeliverable2-main` to `IPCdeliverable2`.

#### PBS script:
1. Connect via SSH to the cluster: ` ssh username@hpc.unitn.it `
2. Upload the project folder into your personal directory on the cluster
3. Go inside the project folder `cd IPCdeliverable2`
4. In the main directory of the project choose the pbs of the method you want to run (ex. `methodMPI_1.pbs`) and open it to change the username of the working directory path (line 17).
5. Subit the job to the queue by running `qsub methodMPI_1.pbs`, the pbs is set up to submit the job to the `short_cpuQ` queue.
6. Wait for the job to run, the job does the compilation and runs the program with every tested matrix size.
The pbs outputs will be saved inside the `/IPCDeliverable2/pbsOutputs/` folder as __methodX.o__ file and the csv files containing all the data will be saved into the `/IPCDeliverable2/methodMPI_X/data/csv` folder. (Swap X with one of the three methods available)

#### Interactive Session: 
1. Connect via ssh to the cluster: ` ssh username@hpc.unitn.it `
2. Upload the project folder to your personal directory on the cluster
3. Start an interactive session: `qsub -I -q short_cpuQ -l select=1:ncpus=64:mpiprocs=64:mem=256mb `
4. Go to the `/IPCDeliverable2/methodMPI_1/src/` folder
5. Run `chmod +x compileMPI.sh` and then run `chmod +x runTestsMPI.sh`  to make the scripts executable
6. Run `./compileMPI.sh` to compile the complete code
7. Run `./runTestsMPI.sh` to execute the program with all the test cases (same as above in the PBS script). 
The data will be printed on the console but it will also be saved in the `/IPCDeliverable2/methodMPI_1/data/csv` folder.


#### Manual execution:
The program can also be run manually with a single matrix size specifying size, to do so run `mpirun -np X ./matTrans Y` where X is the number of processes for MPI (usually also chosen as a power of two between 1/2/4/8/16/32/64) and Y is the size of the matrix (expressed as a power of 2, default=4)

An optional `-mpi` flag can be used to only execute the MPI implementation (by default all the SEQ, OMP and MPI implementations are executed)

Example of execution with 4 mpi processes and matrix size = 2^12, only MPI:`mpirun -np 4 ./matTrans 12 -mpi` 
 

## Plotter
All the graphs used inside the report were generated using the __plotter.py__ Python program found inside the  `/IPCDeliverable2/methodMPI_1/python` folder.
(You can find a plotter.py in each method's folder)
### Reproducibility
(This instructions also apply to every method, example for method1 is shown)
All the testing was done using _Python 3.12.7_ and it runs with the following libraries:
- _Pandas 2.2.2_
- _Matplotlib 3.9.2_
- _Numpy 1.26.4_

Before running the python program you need to run the `/IPCDeliverable2/methodMPI_1/src/runTestsMPI.sh` script so that new data gets generated for every test case needed to generate the graphs (if no data is present inside the `IPCDeliverable2/methodMPI_1/data/csv` folder).

All the graphs generated will be saved into the `IPCDeliverable2/methodMPI_1/data/graphs` folder.
