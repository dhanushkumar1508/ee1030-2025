import ctypes
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

# Load the shared library
lib = ctypes.CDLL("./main.so")  # make sure to compile the C file as liblocus.so

# Define ctypes argument types
lib.compute_locus_check.argtypes = [
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # n1
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # n2
    ctypes.c_double,                                  # d1
    ctypes.c_int,                                     # nt
    np.ctypeslib.ndpointer(dtype=np.float64, ndim=1),# t_values
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # Qs (3 x nt)
    np.ctypeslib.ndpointer(dtype=np.float64, ndim=1),# d_vec (3)
    ctypes.POINTER(ctypes.POINTER(ctypes.c_double)),  # pts (4x3)
    np.ctypeslib.ndpointer(dtype=np.int32, ndim=1)   # truths (4)
]

# ---------- Input data ----------
n1 = np.array([1.0, 2.0, -1.0], dtype=np.float64)
n2 = np.array([2.0, -1.0, 1.0], dtype=np.float64)
d1 = 1.0

# Candidate points a,b,c,d
pts_values = np.array([
    [0, -5/6, -2/3],
    [-1/6, -1/3, 1/6],
    [-5/6, 0, 2/3],
    [-1/3, 0, 2/3]
], dtype=np.float64)

# Number of t values along L
nt = 200
t_values = np.linspace(-1.5, 1.5, nt, dtype=np.float64)

# Allocate memory for Qs (3 x nt)
Qs = (ctypes.POINTER(ctypes.c_double) * 3)()
for i in range(3):
    Qs[i] = (ctypes.c_double * nt)()

# Allocate memory for points array
pts = (ctypes.POINTER(ctypes.c_double) * 4)()
for i in range(4):
    pts[i] = (ctypes.c_double * 3)(*pts_values[i])

# Allocate memory for d_vec and truths
d_vec = np.zeros(3, dtype=np.float64)
truths = np.zeros(4, dtype=np.int32)

# Convert n1, n2 to ctypes pointers
n1_ct = (ctypes.POINTER(ctypes.c_double) * 3)()
n2_ct = (ctypes.POINTER(ctypes.c_double) * 3)()
for i in range(3):
    n1_ct[i] = ctypes.pointer(ctypes.c_double(n1[i]))
    n2_ct[i] = ctypes.pointer(ctypes.c_double(n2[i]))

# Call the C function
lib.compute_locus_check(n1_ct, n2_ct, d1, nt, t_values, Qs, d_vec, pts, truths)

# ---------- Print results ----------
for i, label in enumerate(['A','B','C','D']):
    print(f"Point {label} lies on M? {'Yes' if truths[i]==1 else 'No'}")
print("Direction vector of line L:", d_vec)

# ---------- Plot ----------
fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111, projection='3d')

# Planes
xx, yy = np.meshgrid(np.linspace(-1.5,1.5,20), np.linspace(-1.5,1.5,20))
zz1 = (-d1 - n1[0]*xx - n1[1]*yy)/n1[2]
zz2 = (-(-1) - n2[0]*xx - n2[1]*yy)/n2[2]
ax.plot_surface(xx, yy, zz1, alpha=0.3, color='cyan')
ax.plot_surface(xx, yy, zz2, alpha=0.3, color='orange')

# Line L
t_vals = np.linspace(-1.5,1.5,200)
L_points = np.array([t*d_vec for t in t_vals])
ax.plot(L_points[:,0], L_points[:,1], L_points[:,2], 'r', linewidth=3, label='Line L')

# Line M (from Qs)
M_points = np.array([[Qs[i][k] for k in range(nt)] for i in range(3)]).T
ax.plot(M_points[:,0], M_points[:,1], M_points[:,2], 'g', linewidth=3, label='Line M')

# Plot candidate points
for i, label in enumerate(['A','B','C','D']):
    color = 'blue' if truths[i]==1 else 'red'
    P = pts_values[i]
    ax.scatter(P[0], P[1], P[2], s=120, c=color)
    ax.text(P[0]+0.05, P[1]+0.05, P[2]+0.05, label, fontsize=12)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='cyan', alpha=0.3, label='Plane P1'),
    mpatches.Patch(facecolor='orange', alpha=0.3, label='Plane P2'),
    Line2D([0],[0], color='r', lw=3, label='Line L'),
    Line2D([0],[0], color='g', lw=3, label='Line M'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Point on M'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Point not on M')
]
ax.legend(handles=legend_elements)

ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title("Planes, Line L, Line M, and Points")
ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.5,1.5); ax.set_zlim(-1.5,1.5)
ax.view_init(elev=20, azim=40)

plt.savefig("../figs/planes_lines_points_ctypes.png", dpi=300)
plt.show()

