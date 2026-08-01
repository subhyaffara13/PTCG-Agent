
def E(expr):
    integrate(expr*exponential(x, rate)*normal(y, mu1, sigma1),
                     (x, 0, oo), (y, -oo, oo), meijerg=True)
    integrate(expr*exponential(x, rate)*normal(y, mu1, sigma1),
                     (y, -oo, oo), (x, 0, oo), meijerg=True)

