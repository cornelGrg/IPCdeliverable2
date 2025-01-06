#include "../include/matTrans.h"
#include <iostream>
#include <mpi.h>


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

void matTransposeFlattenedMPI(std::vector<float>& localMatrix, std::vector<float>& transposedMatrix, int n, int rank, int size) {
    // Calcola il numero di righe che ogni processo deve gestire
    int rowsPerProcess = n / size;
    int remainingRows = n % size;  // Le righe rimanenti per i processi rimanenti
    int startRow = rank * rowsPerProcess;
    int endRow = (rank + 1) * rowsPerProcess;

//    if (rank == size - 1) {
//        endRow += remainingRows;  // L'ultimo processo prende anche le righe rimanenti
//    }

    // Prepara un array per la parte della matrice che questo processo gestir�

    //std::vector<float> localtransposedMatrix(rowsPerProcess * n, 0.0f);

    // Scatter: distribuiamo le righe della matrice originale tra i processi
//    MPI_Scatter(flatMatrix.data(), rowsPerProcess * n, MPI_FLOAT, localMatrix.data(), rowsPerProcess * n, MPI_FLOAT, 0, MPI_COMM_WORLD);

    // Trasposizione locale: ognuno dei processi prende le righe e le trasforma in colonne
    for (int i = startRow; i < endRow; ++i) {
        for (int j = 0; j < n; ++j) {
            transposedMatrix[j * n + i] = localMatrix[(i - startRow) * n + j]; //localtransposedMatrix
        }
    }
    //MPI_Gather(localtransposedMatrix.data(), rowsPerProcess * n, MPI_FLOAT, transposedMatrix.data(), rowsPerProcess * n, MPI_FLOAT, 0, MPI_COMM_WORLD);

    // Ogni processo stampa la propria parte della matrice trasposta
    //std::cout << "Processo " << rank << " ha trasposto le righe:\n";
    //for (int i = startRow; i < endRow; ++i) {
    //  for (int j = 0; j < n; ++j) {
    //    std::cout << transposedMatrix[i * n + j] << " ";
    //}
    //std::cout << std::endl;
    //}

    //PER FANE ANDARE MET� TOLGO LA GATHER PIU CH LTRO TENGO COMMENTATA LA GATHER E  TOLGO LA LOCALTRANSPOSITIONMATRIX METTENDO LA TRANSPOSITIONMATRIX
}


