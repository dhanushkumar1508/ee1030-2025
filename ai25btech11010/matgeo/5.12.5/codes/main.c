#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "/home/dhanush-kumar-a/ee1030-2025/ai25btech11010/matgeo/5.12.5/codes/libs/matfun.h"


// Function to solve determinant equation det([[x+3, -2], [-3*x, 2]]) = 8
double solve_det_equation() {
    double **A = createMat(2, 2);

    // We'll solve the equation 2*x^2 = 8, but let's use matrix det
    // Represent matrix as [[x+3, -2], [-3*x, 2]]
    // We'll solve symbolically by using quadratic formula
    double a = 2.0;   // coefficient of x^2
    double b = 0.0;   // coefficient of x
    double c = -8.0;  // constant term
    double **roots = Matquad(a, b, c); // Solve 2*x^2 - 8 = 0

    double x = roots[0][0]; // Return positive root (x ∈ N)
    
    // Free allocated memory
    free(A);
    free(roots);

    return x;
}

// Entry point for Python ctypes
double solve_det_ctypes() {
    return solve_det_equation();
}

int main() {
    double x = solve_det_equation();
    printf("Solution x ∈ N: %lf\n", x);
    return 0;
}

