import ctypes
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the C shared library
lib = ctypes.CDLL("./main.so")

# Define function prototype
lib.solve_system.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # A
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # B
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # C
    ctypes.POINTER(ctypes.c_double)                   # X
]

# Matrices A, B, C
A = np.array([[1,  2, -3],
              [2,  3,  2],
              [3, -3, -4]], dtype=np.double)

B = np.array([[-6, 17, 13],
              [14,  5,  -8],
              [-15, 9, -1]], dtype=np.double)

C = np.array([[-4],
              [ 2],
              [11]], dtype=np.double)

# Convert numpy arrays to ctypes double**
def to_c_matrix(arr):
    return (ctypes.POINTER(ctypes.c_double) * arr.shape[0])(
        *[row.ctypes.data_as(ctypes.POINTER(ctypes.c_double)) for row in arr]
    )

A_c = to_c_matrix(A)
B_c = to_c_matrix(B)
C_c = to_c_matrix(C)

# Output vector X
X = (ctypes.c_double * 3)()
lib.solve_system(A_c, B_c, C_c, X)

# Convert solution to numpy for plotting
solution = np.array([X[i] for i in range(3)])
print("✅ Solution X =", solution)

# -------------------- Plotting --------------------
if not os.path.exists("figs"):
    os.makedirs("figs")

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection="3d")

# Create a grid
xx, yy = np.meshgrid(np.linspace(-10,10,50), np.linspace(-10,10,50))

# Plane 1:  x + 2y - 3z = -4  -> z = (x + 2y + 4)/3
z1 = (xx + 2*yy + 4) / 3
ax.plot_surface(xx, yy, z1, alpha=0.5, color="cyan")

# Plane 2: 2x + 3y + 2z = 2  -> z = (2 - 2x - 3y)/2
z2 = (2 - 2*xx - 3*yy) / 2
ax.plot_surface(xx, yy, z2, alpha=0.5, color="orange")

# Plane 3: 3x - 3y - 4z = 11 -> z = (3*xx - 3*yy - 11)/4
z3 = (3*xx - 3*yy - 11) / 4
ax.plot_surface(xx, yy, z3, alpha=0.5, color="green")

# Plot the solution point
ax.scatter(solution[0], solution[1], solution[2], 
           color="red", s=100, label=f"Solution {solution}")

# Labels
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title("Solution of 3 Planes")
ax.legend()

# Save figure
plt.savefig("../figs/planes_solution1.png", dpi=300)
plt.show()
