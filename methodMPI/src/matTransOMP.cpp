#include "../include/matTrans.h"
#include <iostream>
#include <omp.h>


bool checkSymOMP(const std::vector<std::vector<float>>& mat, int n, int thN){
    bool f = true;
    #pragma omp parallel for collapse(2) num_threads(thN) reduction(&&: f) //reduction on boolean variable to avoid race conditions
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] != mat[j][i]) f = false;
        }
    }
    return f;
}


void matTransposeOMP(std::vector<std::vector<float>>& mat, int n, int thN){ //passed by copy
    #pragma omp parallel for num_threads(thN) //can't collapse since inner for has a dependency on the outer
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {   //only check the upper triangle since mat is square
            std::swap(mat[i][j], mat[j][i]);
        }
    }
}