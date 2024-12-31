#include "../include/support.h"
#include <random>
#include <cmath>
#include <fstream>
#include <iostream>

std::vector<std::vector<float>> matInit(int n, int decimals){
    //random number generator
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_real_distribution<float> distr(0.0f, 10.0f);

    std::vector<std::vector<float>> mat(n, std::vector<float>(n));

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {

            mat[i][j] = std::round(distr(generator) * std::pow(10.0f, decimals)) / std::pow(10.0f, decimals);
        }
    }

    return mat;
}

bool checkTrans(std::vector<std::vector<float>>& M, std::vector<std::vector<float>>& T){
    int size = M.size();

    //random position checker
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<int> distr(0, size - 1);

    for (int i = 0; i < 30; ++i) {
        int x = distr(generator);
        int y = distr(generator);
        if (M[x][y] != T[y][x]) return false;
    }

    return true;
}

void printMatrix(const std::vector<std::vector<float>>& M){
    int size = M.size();
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            std::cout << M[i][j] << "\t";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

void saveToCSV(int id, std::string type, const double time, const int m_size, const std::string& filename){
    //check if file already exists
    std::ifstream fileR(filename);
    bool fileExists = fileR.is_open();

    //open in append mode
    std::ofstream file(filename, std::ios::app);
    if(!file){
        std::cout << "Error: not able to open file :(" << std::endl;
        return;
    }

    //write the csv header
    if(!fileExists){
        if (type == "omp"){
            file << "n_threads;time(s);mPow_size\n";
        }else if (type == "mpi"){
            file << "n_procs;time(s);mPow_size\n";
        }
        else{
            file << "time(s);mPow_size\n";
        }
    }

    if (type == "omp"){
        file << id << ";" << time << ";" << m_size << "\n";
    }else if (type == "mpi"){
        file << id << ";" << time << ";" << m_size << "\n";
    }else{
        file << time << ";" << m_size << "\n";
    }

    file.close();
}

std::vector<float> flatten(const std::vector<std::vector<float>>& mat) {
    std::vector<float> flat;
    for (const auto& row : mat) {
        flat.insert(flat.end(), row.begin(), row.end());
    }
    return flat;
}

std::vector<std::vector<float>> deflatten(const std::vector<float>& flat, int N) {
    std::vector<std::vector<float>> mat(N, std::vector<float>(N));
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            mat[i][j] = flat[i * N + j];
        }
    }
    return mat;
}

void printMatrixFlat(const std::vector<float>& M){
    int size = M.size();
    for (int i = 0; i < size; ++i) {
        std::cout << M[i] << "\t";
    }
    std::cout << std::endl;
}