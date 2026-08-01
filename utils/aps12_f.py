
def aps12_f(x, n):
    r"""nth root of x, with a zero at x=n"""
    return np.power(x, 1.0 / n) - np.power(n, 1.0 / n)

