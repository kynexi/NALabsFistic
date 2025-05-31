import math

def func(x):
    return pow(math.e, x) - pow(x, 2)

def bisection(a, b, eps):
    
    if (func(a) * func(b) >= 0):
        print("You have not assumed right a and b\n")
        return
    c = a

    while ((b-a) >= eps):

        # Find middle point
        c = (a+b)/2
 
        # Check if middle point is root
        if (func(c) == 0.0):
            break
 
        # Decide the side to repeat the steps
        if (func(c)*func(a) < 0):
            b = c
        else:
            a = c     
    print("The value of root is : ", c)

def main():
    eps = 1e-8
    a = -2
    b = 0
    bisection(a, b, eps)

main()
#The value of root is :  -0.7034674224560149