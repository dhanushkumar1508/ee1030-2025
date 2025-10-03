import ctypes

lib = ctypes.CDLL('./libsolve_det.so')  # Shared library compiled from above C code
lib.solve_det_ctypes.restype = ctypes.c_double

x = lib.solve_det_ctypes()
print("Solution x ∈ N:", x)

