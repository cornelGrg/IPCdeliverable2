#include "../include/matTrans.h"
#include "../include/support.h"
#include <iostream>
#include <mpi.h>


int checkSymMPI(const std::vector<float>& mat, int n, int mpi_rank, int mpi_size){
    int rows_per_process = n / mpi_size;
    int rows_reminder = n % mpi_size;

    int start_row = (mpi_rank) * rows_per_process + std::min(mpi_rank, rows_reminder);
    int end_row = start_row + rows_per_process + (mpi_rank < rows_reminder);

    //check assigned portion of matrix
    for (int i = start_row; i < end_row; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i * n + j] != mat[j * n + i]) return 0;
        }
    }
    return 1;
}

void matTransposeMPI(std::vector<float>& localBlock,  int n, int mpi_rank, MPI_Win win, int rowsPerProcess){
    MPI_Win_fence(0, win);

    for (int i = 0; i < rowsPerProcess; ++i) {
        for (int j = 0; j < n; ++j) {
            int globalRow = j;
            int globalCol = mpi_rank * rowsPerProcess + i;
            float value = localBlock[i * n + j];

            MPI_Put(&value, 1, MPI_FLOAT, 0, globalRow * n + globalCol, 1, MPI_FLOAT, win);  //j*n+i
        }
    }

    MPI_Win_fence(0, win);
}


