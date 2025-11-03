# Code by GVV Sharma
# Corrected and improved with point labels

import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
import os

# Direction vectors (column vectors)
m1 = np.array([1, -3, 2])
m2 = np.array([2, 3, 1])

# Points on lines
P1 = np.array([1, 2, 3])
P2 = np.array([4, 5, 6])

# Difference vector
b = P2 - P1

# Construct A matrix
A = np.column_stack((m1, -m2))  # Note: -m2 ensures shortest vector = Q2 - Q1

# Solve for λ₁ and λ₂
x_ls, residuals, rank, s = LA.lstsq(A, b, rcond=None)
lambda1, lambda2 = x_ls

# Closest points on the lines
Q1 = P1 + lambda1 * m1
Q2 = P2 + lambda2 * m2

# Shortest distance
shortest_distance = LA.norm(Q2 - Q1)

print("Closest point on Line 1:", Q1)
print("Closest point on Line 2:", Q2)
print("Shortest distance between lines:", shortest_distance)

# ----- Plotting -----
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

# Plot lines centered around closest points for clarity
t1 = np.linspace(lambda1 - 1, lambda1 + 1, 100)
t2 = np.linspace(lambda2 - 1, lambda2 + 1, 100)
L1 = P1[:, np.newaxis] + m1[:, np.newaxis] * t1
L2 = P2[:, np.newaxis] + m2[:, np.newaxis] * t2

ax.plot3D(L1[0], L1[1], L1[2], 'r', linewidth=2, label='Line 1')
ax.plot3D(L2[0], L2[1], L2[2], 'b', linewidth=2, label='Line 2')

# Plot closest points
ax.scatter(*Q1, color='k', s=60, label='Closest Point Line 1')
ax.scatter(*Q2, color='k', s=60, label='Closest Point Line 2')

# Label points with coordinates
ax.text(Q1[0], Q1[1], Q1[2], f'Q1{tuple(np.round(Q1,2))}', color='k', fontsize=10)
ax.text(Q2[0], Q2[1], Q2[2], f'Q2{tuple(np.round(Q2,2))}', color='k', fontsize=10)

# Plot shortest distance line
ax.plot3D([Q1[0], Q2[0]], [Q1[1], Q2[1]], [Q1[2], Q2[2]], 'g--', linewidth=2, label='Shortest Distance')

# Labels and grid
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.legend()
ax.grid(True)
ax.set_title('Shortest Distance Between Skew Lines')

# Create ../figs folder if it doesn't exist
os.makedirs('../figs', exist_ok=True)

# Save figure
plt.savefig('../figs/6.4.10_skew_lines.png', dpi=300)
plt.show()
