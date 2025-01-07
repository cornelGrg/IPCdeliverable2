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

void matTransposeMPI(std::vector<float>& localMatrix, std::vector<float>& transposedMatrix, int n, int rank, int size) {
    int rowsPerProcess = n / size;
    int startRow = rank * rowsPerProcess;
    int endRow = (rank + 1) * rowsPerProcess;

    // local transpose
    for (int i = startRow; i < endRow; ++i) {
        for (int j = 0; j < n; ++j) {
            transposedMatrix[j * n + i] = localMatrix[(i - startRow) * n + j];
        }
    }
}