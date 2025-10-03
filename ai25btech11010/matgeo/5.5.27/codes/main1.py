import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


# ---------- Define matrices ----------
A = np.array([[1, 2, -3],
              [2, 3, 2],
              [3, -3, -4]], dtype=float)

B = np.array([[-6, 17, 13],
              [14, 5, -8],
              [-15, 9, -1]], dtype=float)

C = np.array([-4, 2, 11], dtype=float)

# ---------- Use AB = 67I3 property ----------
BC = B @ C           # matrix multiplication
X = (1/67) * BC      # solution vector

print("Solution in matrix form:")
print(X.reshape(-1, 1))   # column vector

# ---------- Plotting ----------
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

# Create grid for planes
xx, yy = np.meshgrid(np.linspace(-5, 5, 20),
                     np.linspace(-5, 5, 20))

# Plane 1: x + 2y - 3z = -4  -> z = (x + 2y + 4)/3
z1 = (xx + 2*yy + 4)/3

# Plane 2: 2x + 3y + 2z = 2  -> z = (2 - 2*xx - 3*yy)/2
z2 = (2 - 2*xx - 3*yy)/2

# Plane 3: 3x - 3y - 4z = 11 -> z = (3*xx - 3*yy - 11)/4
z3 = (3*xx - 3*yy - 11)/4

# Plot planes
ax.plot_surface(xx, yy, z1, alpha=0.5, color="red")
ax.plot_surface(xx, yy, z2, alpha=0.5, color="green")
ax.plot_surface(xx, yy, z3, alpha=0.5, color="blue")

# Plot solution point
ax.scatter(X[0], X[1], X[2], color="black", s=80, label="Solution (x,y,z)")

# Labels
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
ax.set_title("Intersection of 3 Planes")

# Legend
custom_lines = [
    plt.Line2D([0], [0], color="red", lw=4),
    plt.Line2D([0], [0], color="green", lw=4),
    plt.Line2D([0], [0], color="blue", lw=4),
    plt.Line2D([0], [0], marker='o', color="w", markerfacecolor="black", markersize=8)
]
ax.legend(custom_lines, ["Plane 1", "Plane 2", "Plane 3", "Solution"])

# Save figure
plt.savefig("../figs/planes_solution.png", dpi=300, bbox_inches="tight")
plt.show()
