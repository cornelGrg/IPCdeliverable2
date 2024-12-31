#include "../include/matTrans.h"
#include "../include/support.h"
#include <omp.h>
#include <algorithm>
#include <mpi.h>
#include <iostream>

//In-Place transposition algorithm
int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int mpi_rank, mpi_size;
    MPI_Comm_rank(MPI_COMM_WORLD, &mpi_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &mpi_size);

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

    for (int m_size: m_sizes) {
        pow = m_size;
        int size = (1 << pow);

        if (size % mpi_size == 0) {


            std::vector <std::vector<float>> M(size, std::vector<float>(size, 0));
            std::vector <std::vector<float>> T(size, std::vector<float>(size, 0));

            if (mpi_rank == 0) {
                M = matInit(size, 3);
                isSym = checkSymSEQ(M, size);

                std::cout << std::endl << "------------------------------------------" << std::endl;
                std::cout << "Matrix size: " << m_size << std::endl;

                //!onlyMPI
                if (!onlyMPI) {
                    //SEQUENTIAL
                    totT = 0.0;
                    if (!isSym) {
                        for (int i = 0; i < 5; ++i) {  //medium time of 5 executions
                            executions++;

                            wt1 = omp_get_wtime();
                            matTransposeSEQ(M, T, size);
                            wt2 = omp_get_wtime();

                            if (!checkTrans(M, T))
                                std::cout << "Error: matrix not transposed properly! (SEQUENTIAL)" << std::endl;

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

                    std::cout << "Sequential: wall clock time (avg of " << executions << ") = " << totT / executions
                              << " sec"
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

                                wt1 = omp_get_wtime();
                                matTransposeOMP(M, T, size, thread);
                                wt2 = omp_get_wtime();

                                if (T != CheckT)
                                    std::cout << "Error: matrix not transposed properly! (OMP)" << std::endl;

                                totT += (wt2 - wt1);
                                saveToCSV(thread, "omp", (wt2 - wt1), pow, OMPcsvFile);
                            }

                            std::cout << thread << "\t  " << (totT / executions) << "\t        (avg of " << executions
                                      << ")"
                                      << std::endl;
                            executions = 0;
                        } else {
                            T = M;
                            std::cout << "Matrix was symmetric against all odds! No transposition required"
                                      << std::endl;
                        }
                    }
                }
            }

            MPI_Barrier(MPI_COMM_WORLD);
            std::vector<float> M_flat(size * size);
            std::vector<float> T_flat(size * size);
            int int_bool_flag;

            if (mpi_rank == 0) {
                std::cout << std::endl << "MPI:" << std::endl;
                std::cout << "N_procs|wall_clock_time (avg)|n_of_executions" << std::endl;
                M_flat = flatten(M);
                totT = 0.0;
                isSym = checkSymMPI(M, size);
                int_bool_flag = isSym ? 1 : 0;
            }

            //Bcast the same simmetry flag to everyone
            MPI_Bcast(&int_bool_flag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            isSym = (int_bool_flag != 0);

            if (!isSym) {
                for (int i = 0; i < 5; ++i) {

                    MPI_Barrier(MPI_COMM_WORLD);
                    if (mpi_rank == 0) {
                        executions++;
                        wt1 = omp_get_wtime();
                    }

                    matTransposeMPI(M_flat, T_flat, size, mpi_rank, mpi_size);

                    MPI_Barrier(MPI_COMM_WORLD);
                    if (mpi_rank == 0) {
                        wt2 = omp_get_wtime();
                        T = deflatten(T_flat, size);

                        if (!checkTrans(M, T)) {
                            std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;
                        }

                        totT += (wt2 - wt1);

                        saveToCSV(mpi_size, "mpi", (wt2 - wt1), pow, MPIcsvFile);
                    }
                }

                if (mpi_rank == 0) {
                    std::cout << mpi_size << "\t  " << (totT / executions) << "\t        (avg of " << executions << ")"
                              << std::endl;
                    executions = 0;
                }

            } else {
                if (mpi_rank == 0) {
                    T = M;
                    std::cout << "Matrix was symmetric against all odds! No transposition required" << std::endl;
                }
            }
        } else{
            if(mpi_rank == 0){
                std::cout << std::endl << "Size of matrix("<< size*size <<") is not divisible by number of procs(" << mpi_size << ")" << std::endl;
            }
        }
    }

    MPI_Finalize();
    return 0;
}