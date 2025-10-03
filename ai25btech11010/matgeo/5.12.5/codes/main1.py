import numpy as np
from sympy import symbols, Eq, solve

# Define the variable
x = symbols('x')

# Define the matrix
A = np.array([[x + 3, -2],
              [-3*x, 2*x]])

# Compute the determinant using sympy
det = (x + 3)*(2*x) - (-2)*(-3*x)

# Equation: determinant = 8
equation = Eq(det, 8)

# Solve the equation
solutions = solve(equation, x)

# Filter for natural numbers
natural_solutions = [sol for sol in solutions if sol.is_real and sol > 0]

print("All solutions:", solutions)
print("Natural number solution(s):", natural_solutions)

