#include "../include/matTrans.h"
#include "../include/support.h"
#include <iostream>
#include <mpi.h>


bool checkSymMPI(const std::vector<std::vector<float>>& mat, int n){

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] != mat[j][i]) return false;
        }
    }
    return true;
}

void matTransposeMPI(std::vector<float>& mat, std::vector<float>& trans, int n, int mpi_rank, int mpi_size){
    int rowsPerProcess = n / mpi_size;
    
    std::vector<float> localBlock(rowsPerProcess * n);

    MPI_Scatter(mat.data(), rowsPerProcess * n, MPI_FLOAT, localBlock.data(), rowsPerProcess * n, MPI_FLOAT, 0, MPI_COMM_WORLD);

    MPI_Win win;
    float* TransposedMatrix = nullptr;

    if (mpi_rank == 0) {
        MPI_Win_allocate(n * n * sizeof(float), sizeof(float), MPI_INFO_NULL, MPI_COMM_WORLD, &TransposedMatrix, &win);
    } else {
        MPI_Win_allocate(0, sizeof(float), MPI_INFO_NULL, MPI_COMM_WORLD, &TransposedMatrix, &win);
    }

    MPI_Win_fence(0, win);

    for (int i = 0; i < rowsPerProcess; ++i) {
        for (int j = 0; j < n; ++j) {
            int globalRow = j;
            int globalCol = mpi_rank * rowsPerProcess + i;
            float value = localBlock[i * n + j];

            MPI_Put(&value, 1, MPI_FLOAT, 0, globalRow * n + globalCol, 1, MPI_FLOAT, win);
        }
    }

    MPI_Win_fence(0, win);

    if (mpi_rank == 0) {
        trans = std::vector<float>(TransposedMatrix, TransposedMatrix + n * n);
    }

    MPI_Win_free(&win);
}


