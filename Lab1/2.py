import cmath

def f(x):
    return x**3 + 2*x**2 + 10*x - 20

def muller(f, x0, x1, x2, tol):
    max_iter = 100

    for _ in range(max_iter):
        h1 = x1 - x0
        h2 = x2 - x1
        δ1 = (f(x1) - f(x0)) / h1
        δ2 = (f(x2) - f(x1)) / h2
        a = (δ2 - δ1) / (h2 + h1)
        b = a*h2 + δ2
        c = f(x2)
        discriminant = cmath.sqrt(b**2 - 4*a*c)

        if abs(b - discriminant) > abs(b + discriminant):
            denominator = b - discriminant
        else:
            denominator = b + discriminant

        dx = -2 * c / denominator
        x3 = x2 + dx

        if abs(dx) < tol:
            return x3

        x0, x1, x2 = x1, x2, x3

    raise Exception("Too many iterations")

root = muller(f, 0, 1, 2, 1e-8)
print(f"Root is: {root:.10f}") 
print(f"f(root) = {f(root):.10e}")
