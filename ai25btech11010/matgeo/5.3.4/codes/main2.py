import ctypes
import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure 'figs' folder exists
os.makedirs("figs", exist_ok=True)

# Load the shared library
lib = ctypes.CDLL("./main.so")

# Define argument types for ctypes
lib.solve_2x2.argtypes = [
    ctypes.c_double, ctypes.c_double,
    ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)
]

# Read input coefficients
a = float(input("Enter value of a: "))
b = float(input("Enter value of b: "))

# Prepare output variables
x = ctypes.c_double()
y = ctypes.c_double()

# Call C function
lib.solve_2x2(a, b, ctypes.byref(x), ctypes.byref(y))

# Extract values
x_val = x.value
y_val = y.value

print(f"Solution from C function:\nx = {x_val}\ny = {y_val}")

# ---------- Plotting ----------

# Generate x values around the solution
x_vals = np.linspace(x_val-5, x_val+5, 400)

# Equation 1: (a*x - b*y) + (a+4b) = 0 -> y = (a*x + (a+4b))/b
y1 = (a*x_vals + (a + 4*b)) / b

# Equation 2: (b*x + a*y) + (b-4a) = 0 -> y = -(b*x + (b-4a))/a
y2 = -(b*x_vals + (b - 4*a)) / a

plt.figure(figsize=(8,6))
plt.plot(x_vals, y1, label=f'Equation 1: {a}x - {b}y + ({a+4*b})=0')
plt.plot(x_vals, y2, label=f'Equation 2: {b}x + {a}y + ({b-4*a})=0')
plt.scatter(x_val, y_val, color='red', s=100, label=f'Solution ({x_val:.2f}, {y_val:.2f})')
plt.xlabel('x')
plt.ylabel('y')
plt.title("Solution of 2x2 Linear System using C Function")
plt.legend()
plt.grid(True)

# Save figure
fig_path = os.path.join("../figs", "equations_solution1.png")
plt.savefig(fig_path, dpi=300)
print(f"Figure saved at: {fig_path}")

plt.show()

