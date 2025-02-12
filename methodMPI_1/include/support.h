#ifndef SUPPORT_H
#define SUPPORT_H
#include <vector>
#include <string>

std::vector<std::vector<float>> matInit(int n, int decimals);
bool checkTrans(std::vector<std::vector<float>>& M, std::vector<std::vector<float>>& T);
void saveToCSV(int id, std::string type, const double time, const int m_size, const std::string& filename);
void printMatrix(const std::vector<std::vector<float>>& M);
std::vector<float> flatten(const std::vector<std::vector<float>>& mat);
std::vector<std::vector<float>> deflatten(const std::vector<float>& flat, int N);
void printMatrixFlat(const std::vector<float>& M);

#endif
