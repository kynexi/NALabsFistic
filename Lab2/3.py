import numpy as np


def newton_Int(x1, y1, z):
    # Initialize k to 1 and Q to a list of zeros to hold the coefficients
    n = len(x1)
    a = y1.copy()
    # Calculate the divided differences using nested loops
    for j in range(1, n):
        for i in range(n-1, j - 1, -1):
            a[i] = (a[i] - a[i - 1]) / (x1[i] - x1[i - j])
    # Calculate the coefficients of the polynomial using the divided differences
    p = a[-1]
    for i in range(n-2, -1, -1):
        p = a[i] + (z - x1[i]) * p
    # Return the value of the polynomial at the given point x
    return p


def lagrange_interp(x, y, x_interp):
    n = len(x)
    y_interp = 0.0
    for j in range(n):
        L = 1.0
        for k in range(n):
            if k != j:
                L *= (x_interp - x[k]) / (x[j] - x[k])
        y_interp += L * y[j]
    return y_interp


def piecewise_linear_interp(x, y, x_interp):
    n = len(x)
    if x_interp <= x[0]:
        return y[0]
    if x_interp >= x[-1]:
        return y[-1]
    for i in range(1, n):
        if x_interp <= x[i]:
            t = (x_interp - x[i - 1]) / (x[i] - x[i - 1])
            y_interp = (1 - t) * y[i - 1] + t * y[i]
            return y_interp


def cubic_spline_interp(x, y, x_interp):
    n = len(x)
    if x_interp <= x[0]:
        return y[0]
    if x_interp >= x[-1]:
        return y[-1]
    h = np.diff(x)
    alpha = np.zeros(n)
    l = np.ones(n)
    c = np.zeros(n)
    b = np.zeros(n)
    d = np.zeros(n)
    for i in range(1, n - 1):
        alpha[i] = h[i] / (h[i - 1] + h[i])
        l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * alpha[i - 1]
        c[i] = h[i] / l[i]
        b[i] = h[i - 1] / l[i - 1]
        d[i] = (3 / (h[i - 1] + h[i])) * (alpha[i - 1] * (y[i + 1] - y[i]) - (alpha[i] * (y[i] - y[i - 1])))
    c[-1] = 0
    for j in range(n - 2, -1, -1):
        c[j] = c[j] - b[j] * c[j + 1]
        d[j] = d[j] - b[j] * d[j + 1]
    index = np.searchsorted(x, x_interp)
    interval = index - 1
    t = (x_interp - x[interval]) / h[interval]
    y_interp = ((d[interval] * t + c[interval]) * t + b[interval]) * t + y[interval]
    return y_interp

def interpolated_function(xi):
    return cubic_spline_interp(known_x, known_y, xi)

def romberg(f, a, b, max_depth=5):
    R = np.zeros((max_depth, max_depth))
    for k in range(max_depth):
        n = 2 ** k
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        fx = np.array([f(xi) for xi in x])
        R[k, 0] = h * (0.5 * fx[0] + np.sum(fx[1:-1]) + 0.5 * fx[-1])
        for j in range(1, k + 1):
            R[k, j] = (4**j * R[k, j - 1] - R[k - 1, j - 1]) / (4**j - 1)
    return R[max_depth - 1, max_depth - 1]


def get_nearest_points(x_data, y_data, target_x, num_points=10):
    combined = sorted(zip(x_data, y_data), key=lambda pair: abs(pair[0] - target_x))
    nearest = combined[:num_points]
    x_near, y_near = zip(*sorted(nearest))  
    return list(x_near), list(y_near)

x1, y1 = [], []
x_missing, missing_indices = [], []

with open("Lab2\\data\\dataset_3.txt") as f:
    lines = f.readlines()

days = 1
for line in lines:
    if line.startswith("Number") or line.startswith("-"):
        continue
    items, time = line.strip().split(",")
    items = int(items)
    if time.strip() == "Nan":
        x_missing.append(items)
        missing_indices.append(days - 1)  # store the index to insert later
        y1.append(None)  # placeholder
    else:
        y1.append(float(time.strip()))
    x1.append(items)
    days += 1


for i, item in enumerate(x_missing):
    print("----------------------------------------------------")
    print(f"Missing #{i+1} at {item} items")
    
    known_x = [x for x, y in zip(x1, y1) if y is not None]
    known_y = [y for y in y1 if y is not None]

    x_near, y_near = get_nearest_points(known_x, known_y, item)

    newton_val = newton_Int(x_near, y_near, item)
    lagrange_val = lagrange_interp(x_near, y_near, item)
    piece_val = piecewise_linear_interp(known_x, known_y, item)
    spline_val = cubic_spline_interp(known_x, known_y, item)

    print(f"Newton: {newton_val:.1f}")
    print(f"Lagrange: {lagrange_val:.1f}")
    print(f"Piecewise: {piece_val:.1f}")
    print(f"Spline: {spline_val:.1f}")

    y1[missing_indices[i]] = spline_val

    known_x = [x for x, y in zip(x1, y1) if y is not None]
    known_y = [y for x, y in zip(x1, y1) if y is not None]

    # Interpolate more points for better area estimation
    x_interp = np.linspace(known_x[0], known_x[-1], num=2 * len(known_x) - 1)
    area = romberg(interpolated_function, known_x[0], item, max_depth=5)
    print(f"Romberg Integration from {known_x[0]} to {item}: {area:.1f} ")
