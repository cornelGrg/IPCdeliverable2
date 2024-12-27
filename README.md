# IPCdeliverable1
![Author](https://img.shields.io/badge/Author-Cornel%20Grigor%20235986-informational)
![Language](https://img.shields.io/badge/C++-8A2BE2)
![Language](https://img.shields.io/badge/Python-green)
![Language](https://img.shields.io/badge/HPC-red)

Repository created for the first deliverable of the "Introduction to Parallel Computing" course at University of Trento, A.A 24/25.

## Assignment
The assignment consists of benchmarking and studying the effects of different parallelization techniques used to optimize a squared matrix transposition. The whole report can be found by opening the __report.pdf__ file.

## Reproducibility
All the tests were done using the University's cluster with _GCC version 9.1.0_.

The main project is written in C++ while the plotter program is written in Python.

Start by downloading the repository, where you can find multiple *methodX* folders, each folder contains a different algorithm that was tested during the making of the report, every algorithm has the same exact folder structure and the instructions below apply to all of them.

- method1: Naive out-of-place matrix transposition algorithm
- method2: Triangular in-place matrix transposition algorithm
- method3: Block-based matrix transposition algorithm

For the best performance overall run *method1*. 
You can find already generated graphs inside every method's graph folder `/methodX/data/graphs/` to see the performance.

### Directory structure
IPCdeliverable1/

```bash
├── method1     #Naive out-of-place
│   ├── build
│   ├── data
│   │   ├── csv
│   │   └── graphs
│   ├── include
│   ├── python
│   └── src
├── method2 #Triangular in-place
│   ├── build
│   ├── data
│   │   ├── csv
│   │   └── graphs
│   ├── include
│   ├── python
│   └── src
├── method3 #Block out-of-place
│   ├── build
│   ├── data
│   │   ├── csv
│   │   └── graphs
│   ├── include
│   ├── python
│   └── src
├── methodComparisonData #Data used to compare the 3 methods and generated graph
└── pbsOutputs
```

### Testing instructions
(These instructions apply to all the 3 methods)
There are two ways to run the program inside the cluster:
Before doing everything clone the repository using `git clone https://github.com/cornelGrg/IPCdeliverable1`

In case you download the zip manually from github.com please rename the folder project from `IPCdeliverable1-main` to `IPCdeliverable1`.

#### PBS script:
1. Connect via SSH to the cluster: ` ssh username@hpc.unitn.it `
2. Upload the project folder into your personal directory on the cluster
3. Go inside the project folder `cd IPCdeliverable1`
4. In the main directory of the project choose the pbs of the method you want to run (ex. `method1.pbs`) and open it to change the username of the working directory path.
5. Subit the job to the queue by running `qsub method1.pbs`, the pbs is set up to submit the job to the `short_cpuQ` queue.
6. Wait for the job to run, the job does the compilation and runs the program with every tested matrix size.
The pbs outputs will be saved inside the `/IPCDeliverable/pbsOutputs/` folder as __methodX.o__ file and the csv files containing all the data will be saved into the `/IPCDeliverable/methodX/data/csv` folder. (Swap X with one of the three methods available)

#### Interactive Session: 
1. Connect via ssh to the cluster: ` ssh username@hpc.unitn.it `
2. Upload the project folder to your personal directory on the cluster
3. Start an interactive session: `qsub -I -q short_cpuQ -l select=1:ncpus=96:ompthreads=96:mem=512mb ` (all tests were conducted using 96 threads in the short_cpuQ queue)
4. Go to the `/IPCDeliverable/method1/src/` folder
5. Run `chmod +x compile.sh` and then run `chmod +x runTests.sh`  to make the scripts executable
6. Run `./compile.sh` to compile the complete code
7. Run `./runTests.sh` to execute the program with all the test cases (same as above in the PBS script). 
The data will be printed on the console but it will also be saved in the `/IPCDeliverable/method1/data/csv` folder.
There is also another test script that was used to test the different implicit compilation flags: `./runTestsOPT.sh`, this can be run in the same way.

**The program can also be run manually with a single matrix size specifying size (expressed as a power of 2, default=4), to do so run `./matTrans 12`  (execution with matrix size = 2^12)**

You can also find the `compileMAC.sh` script in the `/IPCDeliverable/method1/src` folder if you need to run the program with _GCC version 11.5.0_ as this was the first available gcc version available for the 2020+ Apple Silicon MacBooks (this was briefly used for some other testing purposes).
 

## Plotter
All the graphs used inside the report were generated using the __plotter.py__ Python program found inside the  `/IPCDeliverable/method1/python` folder.
(You can find a plotter.py in each method's folder)
### Reproducibility
(This instructions also apply to every method, example for method1 is shown)
All the testing was done using _Python 3.12.7_ and it runs with the following libraries:
- _Pandas 2.2.2_
- _Matplotlib 3.9.2_
- _Numpy 1.26.4_

Before running the python program you need to run the `/IPCDeliverable/method1/src/runTests.sh` script so that new data gets generated for every test case needed to generate the graphs (if no data is present inside the `IPCDeliverable/method1/data/csv` folder).

All the graphs generated will be saved into the `IPCDeliverable/method1/data/graphs` folder.
