import numpy as np
import matplotlib.pyplot as plt
import os

# Create folder 'figs' if it doesn't exist
if not os.path.exists("figs"):
    os.makedirs("figs")

# Coefficients
a = float(input("Enter value of a: "))
b = float(input("Enter value of b: "))

# Coefficient matrix A
A = np.array([[a, -b],
              [b, a]])

# Constants vector
B = np.array([- (a + 4*b),
              4*a - b])

# Determinants
det_A = np.linalg.det(A)
A_x = np.array([[B[0], -b],
                [B[1], a]])
det_Ax = np.linalg.det(A_x)

A_y = np.array([[a, B[0]],
                [b, B[1]]])
det_Ay = np.linalg.det(A_y)

# Solution
x = det_Ax / det_A
y = det_Ay / det_A

print(f"Solution:\nx = {x}\ny = {y}")

# Plotting
x_vals = np.linspace(x-5, x+5, 400)

# Equation 1: (ax - by) + (a+4b)=0 -> y = (ax + a+4b)/b
y1 = (a*x_vals + (a + 4*b)) / b

# Equation 2: (bx + ay) + (b-4a)=0 -> y = -(b*x_vals + b-4a)/a
y2 = -(b*x_vals + (b - 4*a)) / a

plt.figure(figsize=(8,6))
plt.plot(x_vals, y1, label='Equation 1: ax - by + (a+4b)=0')
plt.plot(x_vals, y2, label='Equation 2: bx + ay + (b-4a)=0')
plt.scatter(x, y, color='red', label=f'Solution (x, y)=({x:.2f}, {y:.2f})')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Solution of Equations using Cramer\'s Rule')
plt.legend()
plt.grid(True)

# Save figure
plt.savefig("../figs/equations_solution.png", dpi=300)
plt.show()

