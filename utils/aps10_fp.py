
def aps10_fp(x, n):
    return np.exp(-n * x) * (-n * (x - 1) + 1) + n * x**(n - 1)

