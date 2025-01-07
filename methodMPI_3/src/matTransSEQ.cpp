#include "../include/matTrans.h"
#include <vector>

bool checkSymSEQ(const std::vector<std::vector<float>>& mat, int n){
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] != mat[j][i]) return false;
        }
    }
    return true;
}

void matTransposeSEQ(const std::vector<std::vector<float>>& mat, std::vector<std::vector<float>>& trans, int n){
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            trans[j][i] = mat[i][j];
        }
    }
}

