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

void matTransposeMPI(const std::vector<float>& mat, std::vector<float>& trans, int n, int mpi_rank, int mpi_size) {
    int rows_per_process = n / mpi_size;
    int rows_reminder = n % mpi_size;

    int start_row = mpi_rank * rows_per_process + std::min(mpi_rank, rows_reminder);
    int end_row = start_row + rows_per_process + (mpi_rank < rows_reminder);

    //compute local transpose
    int local_rows = end_row - start_row;
    std::vector<float> local_trans(local_rows * n);

    for (int i = start_row; i < end_row; ++i) {
        for (int j = 0; j < n; ++j) {
            local_trans[(i - start_row) * n + j] = mat[j * n + i];
        }
    }

    //Gather partial results on rank 0
    MPI_Gather(
            local_trans.data(), local_rows * n, MPI_FLOAT, trans.data(), local_rows * n, MPI_FLOAT, 0, MPI_COMM_WORLD
    );
}