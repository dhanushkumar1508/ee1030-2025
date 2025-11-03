#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "/home/dhanush-kumar-a/ee1030-2025/ai25btech11010/matgeo/6.4.10/codes/libs/matfun.h"




void skew_lines_distance(double **P1, double **m1,
                         double **P2, double **m2,
                         double **Q1, double **Q2,
                         double *distance) {
    // Step 1: A = [m1, -m2] (3x2)
    double **neg_m2 = Matscale(m2, 3, 1, -1);
    double **A = Mathstack(m1, neg_m2, 3, 1, 1);
    free(neg_m2);

    // Step 2: b = P2 - P1
    double **b = Matsub(P2, P1, 3, 1);

    // Step 3: Solve least squares λ = (A^T A)^(-1) A^T b
    double **At = transposeMat(A, 3, 2);      // 2x3
    double **AtA = Matmul(At, A, 2, 3, 2);    // 2x2
    double **AtA_inv = Matinv(AtA, 2);        // 2x2
    double **Atb = Matmul(At, b, 2, 3, 1);    // 2x1
    double **lam = Matmul(AtA_inv, Atb, 2, 2, 1);

    double lambda1 = lam[0][0];
    double lambda2 = lam[1][0];

    // Step 4: Compute closest points
    for (int i = 0; i < 3; i++) {
        Q1[i][0] = P1[i][0] + lambda1 * m1[i][0];
        Q2[i][0] = P2[i][0] + lambda2 * m2[i][0];
    }

    // Step 5: Shortest distance
    double **diff = Matsub(Q2, Q1, 3, 1);
    *distance = Matnorm(diff, 3);

    // Free memory
    for (int i = 0; i < 3; i++) free(A[i]);
    free(A);
    for (int i = 0; i < 2; i++) free(At[i]);
    free(At);
    for (int i = 0; i < 2; i++) free(AtA[i]);
    free(AtA);
    for (int i = 0; i < 2; i++) free(AtA_inv[i]);
    free(AtA_inv);
    for (int i = 0; i < 2; i++) free(Atb[i]);
    free(Atb);
    for (int i = 0; i < 2; i++) free(lam[i]);
    free(lam);
    for (int i = 0; i < 3; i++) free(diff[i]);
    free(diff);
}

