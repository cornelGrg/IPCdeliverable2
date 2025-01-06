#ifndef MATTRANS_H
#define MATTRANS_H

#include <vector>

bool checkSymSEQ(const std::vector<std::vector<float>>& mat, int n);
void matTransposeSEQ(std::vector<std::vector<float>>& mat, int n);

bool checkSymOMP(const std::vector<std::vector<float>>& mat, int n, int thN);
void matTransposeOMP(std::vector<std::vector<float>>& mat, int n, int thN);

bool checkSymMPI(const std::vector<std::vector<float>>& mat, int n);
void matTransposeMPI(std::vector<std::vector<float>>& mat, int n);
void matTransposeFlattenedMPI(std::vector<float>& localMatrix, std::vector<float>& transposedMatrix, int n, int rank, int size);
#endif