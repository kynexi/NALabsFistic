import numpy as np
from math import sin, cos, exp, log

# Gauss-Legendre (default interval is [-1, 1])
def gauss_legendre(n):
    x, w = np.polynomial.legendre.leggauss(n)
    return x, w

def gauss_legendre_quad(f, a, b, n, tol):
    x, w = gauss_legendre(n)
    t = 0.5*(x + 1)*(b - a) + a
    gauss_quad = sum(w * f(t)) * 0.5 * (b - a)
    x1, w1 = gauss_legendre(2*n)
    t1 = 0.5*(x1 + 1)*(b - a) + a
    gauss_quad1 = sum(w1 * f(t1)) * 0.5 * (b - a)
    if abs(gauss_quad1 - gauss_quad) < tol:
        return gauss_quad
    else:
        return gauss_legendre_quad(f, a, b, 2*n, tol)

def u_input():
    user_func = input("Function to integrate (use 'x' as variable): ")
    a = float(input("Enter the start of the interval (a): "))
    b = float(input("Enter the end of the interval (b): "))
    tol = float(input("Enter the tolerance (1e-6): "))
    n = 10

    f = np.vectorize(lambda x: eval(user_func, {"x": x, "sin": sin, "cos": cos, "exp": exp, "log": log}))
    result = gauss_legendre_quad(f, a, b, n, tol)
    print(f"The approximate integral of {user_func} from {a} to {b} is: {result}")

# Test
def test():
    tests=[["x**3-2*x**2-5*x",0.1, 10],
        ["x**4-x**3-x**2-x-10", 3,4],
        ["sin(x)+2*exp(x)",1,10],
        ["log(x)+cos(x)-x**3",1,2]]

    for i in tests:
        f=np.vectorize(lambda x:eval(i[0]))
        a,b=i[1],i[2]
        tol=1e-6
        n=10
        print("The result for", i[0], "from",a,"to",b,"is: ", gauss_legendre_quad(f,a,b,n,tol))

def main():
    print("Pick 1 for user input or 2 for test cases")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        u_input()
    elif choice == 2:
        test()
    else:
        print("Invalid choice. Please enter 1 or 2.")

main()
