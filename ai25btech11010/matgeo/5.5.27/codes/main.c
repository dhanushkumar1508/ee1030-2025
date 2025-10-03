#include <stdio.h>
#include <stdlib.h>
#include <math.h>   // <-- Needed for M_PI, cos, sin, sqrt, pow
#include "/home/dhanush-kumar-a/ee1030-2025/ai25btech11010/matgeo/5.5.27/codes/libs/matfun.h"

// Function to solve AX = C using inverse
void solve_system(double **A, double **B, double **C, double *X) {
    // Multiply A and B (3x3 * 3x3)
    double **AB = Matmul(A, B, 3, 3, 3);

    // Check determinant via AB (AB = 67I)
    double det = AB[0][0];  // should be 67
    printf("det(A) via AB: %lf\n", det);

    // A inverse = (1/det) * B
    double **Ainv = createMat(3, 3);
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            Ainv[i][j] = B[i][j] / det;
        }
    }

    // X = A^-1 * C (3x3 * 3x1)
    double **XC = Matmul(Ainv, C, 3, 3, 1);
    for (int i = 0; i < 3; i++) {
        X[i] = XC[i][0];
    }

    // Free memory
    for (int i = 0; i < 3; i++) free(AB[i]);
    free(AB);
    for (int i = 0; i < 3; i++) free(Ainv[i]);
    free(Ainv);
    for (int i = 0; i < 3; i++) free(XC[i]);
    free(XC);
}
