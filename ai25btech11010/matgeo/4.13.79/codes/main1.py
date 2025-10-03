import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

# ---------- Plane normals ----------
n1 = np.array([1, 2, -1], dtype=float)
n2 = np.array([2, -1, 1], dtype=float)

# ---------- Direction vector of L ----------
d = np.cross(n1, n2)
print("Direction vector of L:", d)

# ---------- Line definitions ----------
def rL(t):
    return t * d

def rM(t):
    lam = -1 / np.dot(n1, n1)
    return t*d + lam*n1

# ---------- Option points ----------
A = np.array([0, -5/6, -2/3], dtype=float)
B = np.array([-1/6, -1/3, 1/6], dtype=float)
C = np.array([-5/6, 0, 2/3], dtype=float)
D = np.array([-1/3, 0, 2/3], dtype=float)
points = {"A": A, "B": B, "C": C, "D": D}

# ---------- Check if point lies on M ----------
def is_on_M(P, d, n1, tol=1e-6):
    lam = -1 / np.dot(n1, n1)
    P_shift = P - lam * n1
    t = np.dot(d, P_shift) / np.dot(d, d)
    distance = np.linalg.norm(P_shift - t*d)
    return distance < tol

# ---------- Check points ----------
for label, P in points.items():
    if is_on_M(P, d, n1):
        print(f"Point {label} lies on line M")
    else:
        print(f"Point {label} does NOT lie on line M")

# ---------- Plot ----------
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Planes
xx, yy = np.meshgrid(np.linspace(-1.5, 1.5, 20), np.linspace(-1.5, 1.5, 20))
zz1 = 1 - xx - 2*yy
zz2 = -1 + 2*xx - yy
ax.plot_surface(xx, yy, zz1, alpha=0.3, color='cyan')
ax.plot_surface(xx, yy, zz2, alpha=0.3, color='orange')

# Line L
t_vals = np.linspace(-1.5, 1.5, 200)
L_points = np.array([rL(t) for t in t_vals])
ax.plot(L_points[:,0], L_points[:,1], L_points[:,2], 'r', linewidth=3, label='Line L')

# Line M
M_points = np.array([rM(t) for t in t_vals])
ax.plot(M_points[:,0], M_points[:,1], M_points[:,2], 'g', linewidth=3, label='Line M')

# Plot points with labels
for label, P in points.items():
    color = 'blue' if is_on_M(P, d, n1) else 'red'
    ax.scatter(P[0], P[1], P[2], s=120, c=color)
    ax.text(P[0]+0.05, P[1]+0.05, P[2]+0.05, label, fontsize=12)

# ---------- Create legend manually ----------
legend_elements = [
    mpatches.Patch(facecolor='cyan', edgecolor='cyan', alpha=0.3, label='Plane P1'),
    mpatches.Patch(facecolor='orange', edgecolor='orange', alpha=0.3, label='Plane P2'),
    Line2D([0], [0], color='r', lw=3, label='Line L'),
    Line2D([0], [0], color='g', lw=3, label='Line M'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Point on M'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Point not on M')
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=10)

# Axis labels
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)
ax.set_title("Planes, Line L, Line M, and Points ", fontsize=14)

# Axis limits and grid
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
ax.grid(True)

# Viewing angle
ax.view_init(elev=20, azim=40)

# Ensure directory exists and save figure
os.makedirs("figs", exist_ok=True)
fig_path = os.path.join("../figs", "planes_lines_points.png")
plt.savefig(fig_path, dpi=300)
print(f"Figure saved at: {fig_path}")

plt.show()
