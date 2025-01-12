#ifndef MATTRANS_H
#define MATTRANS_H

#include <vector>
#include <algorithm>

bool checkSymSEQ(const std::vector<std::vector<float>>& mat, int n);
void matTransposeSEQ(const std::vector<std::vector<float>>& mat, std::vector<std::vector<float>>& trans, int n);

bool checkSymOMP(const std::vector<std::vector<float>>& mat, int n, int thN);
void matTransposeOMP(const std::vector<std::vector<float>>& mat, std::vector<std::vector<float>>& trans, int n, int thN);

int checkSymMPI(const std::vector<float>& mat, int n, int mpi_rank, int mpi_size);
void matTransposeMPI(const std::vector<float>& mat, std::vector<float>& local_trans, int n, int start_row, int end_row);
#endif