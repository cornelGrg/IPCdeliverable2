#include "../include/matTrans.h"
#include <iostream>


bool checkSymMPI(const std::vector<std::vector<float>>& mat, int n){
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] != mat[j][i]) return false;
        }
    }
    return true;
}

void matTransposeMPI(std::vector<std::vector<float>>& mat, int n){
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {   //only check the upper triangle since mat is square
            std::swap(mat[i][j], mat[j][i]);
        }
    }
}

