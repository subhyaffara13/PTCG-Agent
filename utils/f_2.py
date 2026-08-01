
def F_2(x, n):
    g = np.zeros([n])
    i = np.arange(2, n+1)
    g[0] = exp(x[0]) - 1
    g[1:] = 0.1*i*(exp(x[1:]) + x[:-1] - 1)
    return g

