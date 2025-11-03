import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from math import sqrt
import os

# --- Define conic: y = x^2  =>  x^T V x + 2u^T x + f = 0 ---
V = np.array([[1.0, 0.0],
              [0.0, 0.0]])          # Matrix V
u = np.array([0.0, -0.5])           # Vector u
f = 0.0                             # Constant term

# --- Define line: y = x  =>  parametric form x = h + k*m ---
h = np.array([0.0, 0.0])            # A point on the line
m = np.array([1.0, 1.0])            # Direction vector

# --- Function definitions ---
def g(h_vec):
    """Compute g(h) = h^T V h + 2u^T h + f"""
    return float(h_vec @ V @ h_vec + 2 * (u @ h_vec) + f)

# Compute required terms
Vh_plus_u = V @ h + u
mT_Vh_u = float(m @ Vh_plus_u)
mT_V_m = float(m @ V @ m)
gh = g(h)

# --- Find κ (kappa) values (intersection parameters) ---
discriminant = mT_Vh_u**2 - mT_V_m * gh
if discriminant < 0:
    print("No real intersection points.")
    kappas = []
else:
    sqrt_disc = sqrt(discriminant)
    k1 = (-mT_Vh_u + sqrt_disc) / mT_V_m
    k2 = (-mT_Vh_u - sqrt_disc) / mT_V_m
    kappas = [k1, k2]

# --- Compute intersection points ---
points = [h + k * m for k in kappas]

print("\n--- Matrix Method Intersection ---")
print("V =\n", V)
print("u =", u)
print("f =", f)
print("m^T (Vh + u) =", mT_Vh_u)
print("m^T V m =", mT_V_m)
print("g(h) =", gh)
print("Discriminant =", discriminant)
print("Kappa values =", kappas)
print("Intersection points:")
for p in points:
    print(f"({p[0]:.2f}, {p[1]:.2f})")

# --- Compute Area between y = x and y = x^2 ---
x = sp.symbols('x')
area_expr = sp.integrate(x - x**2, (x, 0, 1))
area_val = float(area_expr)
print("\nArea enclosed between y = x and y = x^2 =", area_val, "=", sp.Rational(area_expr))

# --- Plotting the curves ---
x_vals = np.linspace(-0.2, 1.2, 400)
y_line = x_vals
y_parabola = x_vals**2

plt.figure(figsize=(6, 6))
plt.plot(x_vals, y_line, label='y = x', color='blue')
plt.plot(x_vals, y_parabola, label='y = x²', color='red')

# Shade area between curves
plt.fill_between(x_vals, y_line, y_parabola, where=(x_vals >= 0) & (x_vals <= 1),
                 color='lightgreen', alpha=0.6)

# Mark intersection points
for p in points:
    plt.plot(p[0], p[1], 'ko')
    plt.text(p[0] + 0.02, p[1] - 0.05, f'({p[0]:.1f}, {p[1]:.1f})')

plt.title("Intersection and Area between y = x and y = x² (Matrix Method)")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.axis('equal')

save_path = "../figs/matrix_intersection_area.png"
plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"\n Figure saved as: {save_path}")

plt.show()

