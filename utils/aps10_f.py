
def aps10_f(x, n):
    r"""Exponential plus a polynomial"""
    return np.exp(-n * x) * (x - 1) + x**n

