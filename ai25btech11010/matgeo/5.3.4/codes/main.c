#include <stdio.h>
#include <stdlib.h>

// Function to solve 2x2 linear system using Cramer's rule
// Equations: 
// (a*x - b*y) + (a+4b) = 0
// (b*x + a*y) + (b-4a) = 0
// Inputs: a, b
// Outputs: x, y (via pointers)
void solve_2x2(double a, double b, double *x, double *y) {
    // Coefficient matrix
    double det = a*a + b*b;  // det = a*a + b*b

    if(det == 0) {
        // Singular system, return NaN
        *x = 0.0/0.0;
        *y = 0.0/0.0;
        return;
    }

    // Determinants for x and y
    double det_x = -((a + 4*b)*a + (b - 4*a)*b);
    double det_y = ((a + 4*b)*b - (b - 4*a)*a);

    *x = det_x / det;
    *y = det_y / det;
}

