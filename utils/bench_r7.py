import random

def bench_R7():
    "[f.subs(x, random()) for _ in range(10**4)]"
    f = x**24 + 34*x**12 + 45*x**3 + 9*x**18 + 34*x**10 + 32*x**21
    [f.subs(x, random()) for _ in range(10**4)]

