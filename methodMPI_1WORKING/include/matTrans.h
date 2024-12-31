#ifndef MATTRANS_H
#define MATTRANS_H

#include <vector>

bool checkSymSEQ(const std::vector<std::vector<float>>& mat, int n);
void matTransposeSEQ(std::vector<std::vector<float>>& mat, std::vector<std::vector<float>>& trans, int n);

bool checkSymOMP(const std::vector<std::vector<float>>& mat, int n, int thN);
void matTransposeOMP(std::vector<std::vector<float>>& mat, std::vector<std::vector<float>>& trans, int n, int thN);

bool checkSymMPI(const std::vector<std::vector<float>>& mat, int n);
void matTransposeMPI(std::vector<float>& mat, std::vector<float>& trans, int n, int mpi_rank, int mpi_size);
#endif