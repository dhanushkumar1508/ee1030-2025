import ctypes
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the shared C library
lib = ctypes.CDLL("./skew_lines.so")

# Define argument types for the C function
lib.skew_lines_distance.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # P1
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # m1
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # P2
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # m2
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # Q1
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # Q2
    ctypes.POINTER(ctypes.c_double)                   # distance
]

# Helper: convert 3x1 numpy array to ctypes double**
def to_c_mat(vec):
    arr = (ctypes.POINTER(ctypes.c_double) * 3)()
    for i in range(3):
        arr[i] = (ctypes.c_double * 1)(vec[i, 0])
    return arr

# Input line points and direction vectors
P1 = np.array([[1], [2], [3]], dtype=np.double)
m1 = np.array([[1], [-3], [2]], dtype=np.double)
P2 = np.array([[4], [5], [6]], dtype=np.double)
m2 = np.array([[2], [3], [1]], dtype=np.double)

# Output matrices
Q1 = np.zeros((3, 1), dtype=np.double)
Q2 = np.zeros((3, 1), dtype=np.double)
distance = ctypes.c_double()

# Convert to ctypes
P1_c = to_c_mat(P1)
m1_c = to_c_mat(m1)
P2_c = to_c_mat(P2)
m2_c = to_c_mat(m2)
Q1_c = to_c_mat(Q1)
Q2_c = to_c_mat(Q2)

# Call the C function
lib.skew_lines_distance(P1_c, m1_c, P2_c, m2_c, Q1_c, Q2_c, ctypes.byref(distance))

# Convert results back to numpy
for i in range(3):
    Q1[i,0] = Q1_c[i][0]
    Q2[i,0] = Q2_c[i][0]

print("Closest point on Line 1:", Q1.ravel())
print("Closest point on Line 2:", Q2.ravel())
print("Shortest distance:", distance.value)

# --------- Improved Plotting ---------
fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

# Line parameters for plotting
t1 = np.linspace(-2, 4, 200)
t2 = np.linspace(-2, 4, 200)

L1 = P1 + m1 * t1
L2 = P2 + m2 * t2

# Plot lines
ax.plot(L1[0], L1[1], L1[2], 'r', linewidth=3, label='Line 1')
ax.plot(L2[0], L2[1], L2[2], 'b', linewidth=3, label='Line 2')

# Plot closest points
ax.scatter(*Q1.ravel(), color='k', s=80, label='Closest Point Line 1')
ax.scatter(*Q2.ravel(), color='k', s=80, label='Closest Point Line 2')

# Label closest points with coordinates
ax.text(Q1[0,0], Q1[1,0], Q1[2,0],
        f'Q1{tuple(np.round(Q1.ravel(),2))}', color='k', fontsize=10)
ax.text(Q2[0,0], Q2[1,0], Q2[2,0],
        f'Q2{tuple(np.round(Q2.ravel(),2))}', color='k', fontsize=10)

# Draw shortest distance
ax.plot([Q1[0,0], Q2[0,0]],
        [Q1[1,0], Q2[1,0]],
        [Q1[2,0], Q2[2,0]],
        'g--', linewidth=3, label=f'Shortest Distance = {distance.value:.2f}')

# Set axis labels
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)
ax.set_title('Shortest Distance Between Skew Lines', fontsize=14)

# Set aspect ratio for better clarity
max_range = np.array([L1[0].max()-L1[0].min(),
                      L1[1].max()-L1[1].min(),
                      L1[2].max()-L1[2].min()]).max() / 2.0

mid_x = (L1[0].max()+L1[0].min()) * 0.5
mid_y = (L1[1].max()+L1[1].min()) * 0.5
mid_z = (L1[2].max()+L1[2].min()) * 0.5

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.legend(fontsize=10)
ax.grid(True)

# Save figure
plt.savefig('../figs/skew_lines_plot1.png', dpi=300)
plt.show()
