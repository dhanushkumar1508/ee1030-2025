#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "/home/dhanush-kumar-a/ee1030-2025/ai25btech11010/matgeo/4.13.79/codes/libs/matfun.h"

// Compute locus M and check candidate points
void compute_locus_check(
    double **n1, double **n2, double d1,
    int nt, double *t_values,
    double **Qs,       // 3 x nt
    double *d_vec,     // 3x1 line direction
    double **pts, int *truths // 4 candidate points
){
    // Step 1: Compute line direction d = n1 x n2
    d_vec[0] = n1[1][0]*n2[2][0] - n1[2][0]*n2[1][0];
    d_vec[1] = n1[2][0]*n2[0][0] - n1[0][0]*n2[2][0];
    d_vec[2] = n1[0][0]*n2[1][0] - n1[1][0]*n2[0][0];

    // Normalize d_vec
    double norm_d = sqrt(d_vec[0]*d_vec[0] + d_vec[1]*d_vec[1] + d_vec[2]*d_vec[2]);
    for(int i=0;i<3;i++) d_vec[i] /= norm_d;

    // Step 2: Compute locus points Qs for each t
    for(int k=0;k<nt;k++){
        double t = t_values[k];
        double **P = createMat(3,1);
        for(int i=0;i<3;i++) P[i][0] = t * d_vec[i];

        // Foot of perpendicular to plane P1: Q = P - lambda*n1
        double lam = (Matdot(n1,P,3) + d1) / Matdot(n1,n1,3); // note +d1 since plane: n^T x + d = 0
        double **Q = Matsub(P, Matscale(n1,3,1,lam), 3,1);

        // Save Q to Qs
        for(int i=0;i<3;i++) Qs[i][k] = Q[i][0];

        // Free temporary matrices
        for(int i=0;i<3;i++) free(P[i]);
        free(P);
        for(int i=0;i<3;i++) free(Q[i]);
        free(Q);
    }

    // Step 3: Check candidate points a,b,c,d
    for(int p=0;p<4;p++){
        double *pt = pts[p];

        // Solve t and lambda from rM = t*d + lambda*n1
        double t_num = pt[0]*d_vec[0] + pt[1]*d_vec[1] + pt[2]*d_vec[2];
        double t_den = d_vec[0]*d_vec[0] + d_vec[1]*d_vec[1] + d_vec[2]*d_vec[2];
        double t = t_num / t_den;

        double lambda_num = n1[0][0]*(pt[0]-t*d_vec[0]) +
                            n1[1][0]*(pt[1]-t*d_vec[1]) +
                            n1[2][0]*(pt[2]-t*d_vec[2]);
        double lambda_den = Matdot(n1,n1,3);
        double lam = lambda_num / lambda_den;

        // Projected point on M
        double xM = t*d_vec[0] + lam*n1[0][0];
        double yM = t*d_vec[1] + lam*n1[1][0];
        double zM = t*d_vec[2] + lam*n1[2][0];

        // Check if close to original point
        double eps = 1e-6;
        truths[p] = (fabs(xM-pt[0])<eps && fabs(yM-pt[1])<eps && fabs(zM-pt[2])<eps) ? 1 : 0;
    }
}
