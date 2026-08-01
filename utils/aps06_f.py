
def aps06_f(x, n):
    r"""Exponential rapidly changing from -1 to 1 at x=0"""
    return 2 * x * np.exp(-n) - 2 * np.exp(-n * x) + 1

