#include "../include/matTrans.h"
#include <iostream>
#include <omp.h>


bool checkSymOMP(const std::vector<std::vector<float>>& mat, int n, int thN){
    bool f = true;
    #pragma omp parallel for collapse(2) num_threads(thN) reduction(&&: f)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] != mat[j][i]) f = false;
        }
    }
    return f;
}


void matTransposeOMP(std::vector<std::vector<float>>& mat, std::vector<std::vector<float>>& trans, int n, int thN){
    #pragma omp parallel for collapse(2) num_threads(thN)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            trans[j][i] = mat[i][j];
        }
    }
}