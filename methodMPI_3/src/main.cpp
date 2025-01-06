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
        int rowsPerProcess = size / mpi_size;
        std::vector<float> M_flat(size*size, 0);
        std::vector<float> T_flat(size*size, 0);
        std::vector<float> localMatrix(rowsPerProcess*size, 0.0f);
        std::vector<float> localTransposedMatrix(rowsPerProcess*size, 0.0f);
        std::vector<float> flatFinal(size*size, 0);

        std::vector<float> global_vector(size*size, 0.0f);

        M_flat = flatten(M);


        if (mpi_rank == 0) {
            std::cout << std::endl << "MPI:" << std::endl;
            std::cout << "N_procs|wall_clock_time (avg)|n_of_executions" << std::endl;
//            M_flat = flatten(M);
//            std::vector<std::vector<float>> M_deflat = deflatten(M_flat, size);

//            if(M == M_deflat){
//                std::cout << "Matrices OG and Flatteend are equal" << std::endl;
//            }else{
//                std::cout << "Matrices OG and Flatteend are NOT equal!!!! ERROR" << std::endl;
//            }
        }


        totT = 0.0;
        isSym = checkSymMPI(M, size);
        if (!isSym) {
            for (int i = 0; i < 1; ++i) {
                executions++;

                MPI_Barrier(MPI_COMM_WORLD);
                wt1 = omp_get_wtime();


                MPI_Scatter(M_flat.data(), rowsPerProcess * size, MPI_FLOAT, localMatrix.data(), rowsPerProcess * size, MPI_FLOAT, 0, MPI_COMM_WORLD);
                matTransposeFlattenedMPI(localMatrix ,T_flat ,size ,mpi_rank ,mpi_size);
                MPI_Reduce(T_flat.data(), global_vector.data(), size*size, MPI_FLOAT, MPI_SUM, 0, MPI_COMM_WORLD);

//                MPI_Alltoall(local_block.data(), block_rows * block_cols / size, MPI_FLOAT,transposed_block.data(), block_rows * block_cols / size, MPI_FLOAT, MPI_COMM_WORLD);
//              MPI_Gather(localTransposedMatrix.data(), size*size/mpi_size, MPI_FLOAT,T_flat.data(), size*size/mpi_size, MPI_FLOAT, 0, MPI_COMM_WORLD);

                MPI_Barrier(MPI_COMM_WORLD);
                wt2 = omp_get_wtime();

                if (mpi_rank == 0) {
//                    printMatrix(M);
//ˆ
                    std::cout << std::endl;
////
                    T = deflatten(T_flat, size);
//                    printMatrix(T);


//                  T != CheckT
//                    if (!checkTrans(M, T)) std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;
                }
                MPI_Barrier(MPI_COMM_WORLD);
                if (mpi_rank == 1) {
//                    printMatrix(M);
//
                    std::cout << std::endl;
////
                    T = deflatten(T_flat, size);
//                    printMatrix(T);
//
////                  T != CheckT
//                    if (!checkTrans(M, T)) std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;
                }
                MPI_Barrier(MPI_COMM_WORLD);
                if (mpi_rank == 2) {
//                    printMatrix(M);
//
                    std::cout << std::endl;
////
                    T = deflatten(T_flat, size);
//                    printMatrix(T);
//
////                  T != CheckT
//                    if (!checkTrans(M, T)) std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;
                   }
                   MPI_Barrier(MPI_COMM_WORLD);

                if (mpi_rank == 3) {
//                    printMatrix(M);
//
                    std::cout << std::endl;
////
                    T = deflatten(T_flat, size);
//                    printMatrix(T);
//
////                  T != CheckT
//                    if (!checkTrans(M, T)) std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;
                }
                MPI_Barrier(MPI_COMM_WORLD);
                if (mpi_rank == 0) {
                    std::cout << std::endl;
////
                    T = deflatten(global_vector, size);
//                    printMatrix(T);


//                  T != CheckT
                    if (!checkTrans(M, T)){ std::cout << "Error: matrix not transposed properly! (MPI)" << std::endl;
                    }else{
                        std::cout << "CONGRATULATION: matrix TRANSPOSED properly! (MPI)" << std::endl;
                    }
                }
                MPI_Barrier(MPI_COMM_WORLD);


                totT += (wt2 - wt1);
                if (mpi_rank == 0) {
                    saveToCSV(mpi_size, "mpi", (wt2 - wt1), pow, MPIcsvFile);
                }
            }

            if (mpi_rank == 0) {
                std::cout << mpi_size << "\t  " << (totT / executions) << "\t        (avg of " << executions << ")"
                          << std::endl;
                executions = 0;
            }


        }else {
            T = M;
            std::cout << "Matrix was symmetric against all odds! No transposition required" << std::endl;
        }

    }

    MPI_Finalize();
    return 0;
}