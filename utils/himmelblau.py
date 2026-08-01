
def himmelblau(p):
    """
    R^2 -> R^1 test function for optimization. The function has four local
    minima where himmelblau(xopt) == 0.
    """
    x, y = p
    a = x*x + y - 11
    b = x + y*y - 7
    return a*a + b*b

