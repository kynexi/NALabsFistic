import matplotlib.pyplot as plt
import numpy as np

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
#Newton's Method

def divided_differences(x, y):
    n = len(x)
    coef = np.copy(y).astype(float)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x[i] - x[i - j])
    return coef

def newton_eval(x_data, coef, x_interp):
    n = len(coef)
    result = coef[-1]
    for i in range(n - 2, -1, -1):
        result = result * (x_interp - x_data[i]) + coef[i]
    return result

def newton_interpolate_missing_values(x_all, y_all, window_size=4):
    x_interp, y_interp = [], []
    for i in range(len(y_all)):
        if not y_all[i] == y_all[i]:  # NaN
            # Find surrounding known points for interpolation
            known = [(x_all[j], y_all[j]) for j in range(len(y_all)) if y_all[j] == y_all[j]]
            # Choose nearest `window_size` known values around the missing point
            known.sort(key=lambda pt: abs(pt[0] - x_all[i]))
            selected = known[:window_size]
            selected_x = [pt[0] for pt in selected]
            selected_y = [pt[1] for pt in selected]
            coef = divided_differences(selected_x, selected_y)
            y_all[i] = newton_eval(selected_x, coef, x_all[i])
            x_interp.append(x_all[i])
            y_interp.append(y_all[i])
    return x_interp, y_interp


x_all, y_all = [], []
with open("Lab2\\data\\dataset_2.txt") as f:
    lines = f.readlines()

day = 1
for line in lines:
    if line.startswith("Date"):
        continue
    date, visitors = line.strip().split(",")
    x_all.append(day)
    y_all.append(float('nan') if visitors == 'Nan' else int(visitors))
    day += 1

# Copy original data for linear interpolation
x_linear, y_linear = x_all[:], y_all[:]

#linear interpolation

x_interp_linear, y_interp_linear = [], []
for i in range(len(y_linear)):
    if not y_linear[i] == y_linear[i]:  # NaN
        # Find neighbors
        j = i - 1
        while j >= 0 and not y_linear[j] == y_linear[j]:
            j -= 1
        k = i + 1
        while k < len(y_linear) and not y_linear[k] == y_linear[k]:
            k += 1
        if j >= 0 and k < len(y_linear):
            y = piecewise_linear_interp([x_linear[j], x_linear[k]], [y_linear[j], y_linear[k]], x_linear[i])
            y_linear[i] = y
            x_interp_linear.append(x_linear[i])
            y_interp_linear.append(y)

#newton interpolation
x_all_for_newton, y_all_for_newton = x_all[:], y_all[:]
x_interp_newton, y_interp_newton = newton_interpolate_missing_values(x_all_for_newton, y_all_for_newton, window_size=4)

plt.figure(figsize=(12, 6))
plt.plot(x_all, [y if y == y else None for y in y_all], 'k-', label="Original data")
plt.plot(x_interp_linear, y_interp_linear, 'ro', label="Linear interpolation")
plt.plot(x_interp_newton, y_interp_newton, 'bs', label="Newton interpolation")
plt.legend()
plt.xlabel("Day")
plt.ylabel("Number of Visitors")
plt.grid(True)
plt.tight_layout()
plt.show()