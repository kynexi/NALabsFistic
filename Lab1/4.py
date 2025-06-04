import numpy as np
from math import sin, cos, exp, log, sqrt

def hybrid_secant_bisection(f, a, b, tol, max_iter):

    iter_count = 0
    x0 = a
    x1 = b

    while iter_count < max_iter:
        f0 = f(x0)
        f1 = f(x1)

        # If slope would be zero, just return x1
        if f1 == f0: #avoid division by zero
            return x1

        # 1) Secant step
        df_dx1 = (f1 - f0) / (x1 - x0)
        x_next = x1 - f1 / df_dx1

        # 2) If secant leaves [a, b], use midpoint instead
        if x_next < a or x_next > b:
            x_next = 0.5 * (a + b)

        # 3) Check convergence
        if abs(f(x_next)) < tol:
            return x_next

        # 4) Shift points for next iteration
        x0 = x1
        x1 = x_next
        iter_count += 1

    # If we exhaust max_iter, return last x1
    return x1


def u_input():
    func_str = input("Enter f(x) in terms of x (e.g. exp(x) - x**3 + 2*x**4):\n").strip()

    def f(x):
        return eval(
            func_str,
            {
                "x": x,
                "sin": sin,
                "cos": cos,
                "exp": exp,
                "log": log,
                "sqrt": sqrt
            }
        )

    a = float(input("Enter lower bound a: "))
    b = float(input("Enter upper bound b: "))
    tol = float(input("Enter tolerance (e.g. 1e-6): "))
    max_iter = int(input("Enter maximum number of iterations: "))

    try:
        fa = f(a)
        fb = f(b)
        if fa * fb > 0:
            print("Warning: f(a) and f(b) may not bracket a root.")
    except Exception as e:
        print("Error evaluating f at a or b:", e)
        return

    root = hybrid_secant_bisection(f, a, b, tol, max_iter)
    print(f"\nApproximate root: {root}")
    print(f"f(root) = {f(root)}")


def test():
    tests = [
        # 1) Solve x^2 - 2 = 0 on [0, 2]
        ("x**2 - 2", 0.0, 2.0, 1e-6, 100),
        # 2) Solve cos(x) - x = 0 on [0, 1]
        ("cos(x) - x", 0.0, 1.0, 1e-6, 100),
        # 3) Solve exp(x) - 3 = 0 on [0, 2]
        ("exp(x) - 3", 0.0, 2.0, 1e-8, 100),
        # 4) Solve sin(x) - 0.5 = 0 on [0, 2]
        ("sin(x) - 0.5", 0.0, 2.0, 1e-6, 100)
    ]

    for i, (func_str, a, b, tol, max_iter) in enumerate(tests, start=1):
        def f(x):
            return eval(
                func_str,
                {
                    "x": x,
                    "sin": sin,
                    "cos": cos,
                    "exp": exp,
                    "log": log,
                    "sqrt": sqrt
                }
            )

        print(f"Test #{i}: f(x) = {func_str}, bracket = [{a}, {b}], tol = {tol}")
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            print("  Warning: f(a) and f(b) may not bracket a root.")
        root = hybrid_secant_bisection(f, a, b, tol, max_iter)
        print(f"  Approximate root: {root}")
        print(f"  f(root) = {f(root)}\n")


def main():
    print("Pick 1 for user input or 2 for test cases")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        u_input()
    elif choice == 2:
        test()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
