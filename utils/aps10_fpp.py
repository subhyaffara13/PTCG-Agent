
def aps10_fpp(x, n):
    return (np.exp(-n * x) * (-n * (-n * (x - 1) + 1) + -n * x)
            + n * (n - 1) * x**(n - 2))

