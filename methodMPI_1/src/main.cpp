#include "../include/matTrans.h"
#include "../include/support.h"
#include <omp.h>
#include <mpi.h>
#include <iostream>

//In-Place transposition algorithm
int main(int argc, char** argv) {
    bool isSym = false;
    bool onlyMPI = false;
    double wt1, wt2, totT;
    int executions = 0;
    std::string MPIcsvFile = "../data/csv/MPItime.csv";
    std::string OMPcsvFile = "../data/csv/OMPtime.csv";
    std::string SEQcsvFile = "../data/csv/SEQtime.csv";
    std::vector<int> threads = {1, 2, 4, 8, 16, 32, 64, 96};
    std::vector<int> m_sizes = {4, 5, 6, 7, 8, 9, 10, 11, 12};

    int pow = 4; //default value

    if (argc > 1) {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];

            if (arg == "-mpi") {
                onlyMPI = true; // Enable MPI mode
            } else {
                try {
                    // Attempt to parse an integer for matrix size
                    pow = std::stoi(arg);
                    m_sizes = {pow}; // Replace m_sizes with single size
                } catch (const std::invalid_argument &) {
                    std::cerr << "Invalid argument: " << arg
                              << ". Expected '-mpi', '-sym', or an integer matrix size."
                              << std::endl;
                    return 1; // Exit with error code
                }
            }
        }
    }

    MPI_Init(&argc, &argv);

    int mpi_rank, mpi_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);


    for (int m_size: m_sizes) {
        pow = m_size;
        int size = (1 << pow);

        std::vector <std::vector<float>> M = matInit(size, 3);
        std::vector <std::vector<float>> T(size, std::vector<float>(size));
        isSym = checkSymSEQ(M, size);

        if (mpi_rank == 0) {
            std::cout << std::endl << "------------------------------------------" << std::endl;
            std::cout << "Matrix size: "<< m_size << std::endl;

            //!onlyMPI
            if (!onlyMPI) {
                //SEQUENTIAL
                totT = 0.0;
                if (!isSym) {
                    for (int i = 0; i < 5; ++i) {  //medium time of 5 executions
                        executions++;

                        T = M; //Support copy for running in-place transposition

                        wt1 = omp_get_wtime();
                        matTransposeSEQ(T, size);
                        wt2 = omp_get_wtime();

                        if (!checkTrans(M, T)) std::cout << "Error: matrix not transposed properly! (SEQUENTIAL)" << std::endl;

                        totT += (wt2 - wt1);
                        saveToCSV(1, "seq", (wt2 - wt1), pow, SEQcsvFile);

                        //printMatrix(M);
                        //printMatrix(T);
                    }
                } else {
                    T = M;
                    std::cout << "Matrix was symmetric against all odds! No transposition required" << std::endl;
                }

                std::vector <std::vector<float>> CheckT = T; //support matrix for checking if imp/omp match the serial transposed

                std::cout << "Sequential: wall clock time (avg of " << executions << ") = " << totT / executions << " sec"
                          << std::endl;
                executions = 0;

                //OpenMP
                std::cout << std::endl << "OpenMP:" << std::endl;
                std::cout << "N_threads|wall_clock_time (avg)|n_of_executions" << std::endl;

                for (int thread: threads) {
                    totT = 0.0;
                    isSym = checkSymOMP(M, size, thread);
                    if (!isSym) {
                        for (int i = 0; i < 5; ++i) {
                            executions++;

                            T = M; //Support copy for running in-place transposition

                            wt1 = omp_get_wtime();
                            matTransposeOMP(T, size, thread);
                            wt2 = omp_get_wtime();

                            if (T != CheckT) std::cout << "Error: matrix not transposed properly! (OMP)" << std::endl;

                            totT += (wt2 - wt1);
                            saveToCSV(thread, "omp", (wt2 - wt1), pow, OMPcsvFile);
                        }

                        std::cout << thread << "\t  " << (totT / executions) << "\t        (avg of " << executions << ")"
                                  << std::endl;
                        executions = 0;
                    } else {
                        T = M;
                        std::cout << "Matrix was symmetric against all odds! No transposition required" << std::endl;
                    }
                }
            }
        }

        MPI_Barrier(MPI_COMM_WORLD);

        //MPI
        if (mpi_rank == 0) {
            std::cout << std::endl << "MPI:" << std::endl;
            std::cout << "N_procs|wall_clock_time (avg)|n_of_executions" << std::endl;
//            printMatrix(M);

//            std::cout << "|||||||||||||||||||||||||||||||" << std::endl;

            std::vector<float> M_flat = flatten(M);
//            printMatrixFlat(M_flat);

//            std::cout << "|||||||||||||||||||||||||||||||" << std::endl;

            std::vector<std::vector<float>> M_deflat = deflatten(M_flat);

//            printMatrix(M_deflat);


//            std::cout << "|||||||||||||||||||||||||||||||" << std::endl;

            if(M == M_deflat){
                std::cout << "Matrices OG and Flatteend are equal" << std::endl;
            }else{
                std::cout << "Matrices OG and Flatteend are NOT equal!!!! ERROR" << std::endl;
            }
        }

        int npMPI = mpi_size;

        totT = 0.0;
        isSym = checkSymMPI(M, size);
        if (!isSym) {
            for (int i = 0; i < 5; ++i) {
                executions++;

                T = M; //Support copy for running in-place transposition

                wt1 = omp_get_wtime();
                matTransposeMPI(T, size);
                wt2 = omp_get_wtime();

                //T != CheckT
                if (!checkTrans(M, T)) std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;

                totT += (wt2 - wt1);
                if (mpi_rank == 0) {
                    saveToCSV(npMPI, "mpi", (wt2 - wt1), pow, MPIcsvFile);
                }
            }

            //ADD -np parameter
            std::cout << npMPI << "\t  " << (totT / executions) << "\t        (avg of " << executions << ")" << std::endl;
            executions = 0;
        }else {
            T = M;
            std::cout << "Matrix was symmetric against all odds! No transposition required" << std::endl;
        }

    }

    MPI_Finalize();
    return 0;
}