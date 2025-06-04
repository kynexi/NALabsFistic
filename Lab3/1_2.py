import numpy as np

# Define system
A = np.array([
    [2, -1],
    [3,  2],
    [1,  1],
    [4, -1],
    [1, -3]
])

b = np.array([4, 7, 3, 1, -2])

# Least squares solution
x_approx, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

print("Approximate (x, y):", x_approx)

# Calculate individual errors per equation
errors = np.abs(A @ x_approx - b)

# Determine stepping order (smallest error first)
order = np.argsort(errors)

# Output
print("Equation errors:", errors)
print("Stepping order (stone numbers):", order + 1)
