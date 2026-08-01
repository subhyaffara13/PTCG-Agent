
def F_6(x, n):
    c = 0.9
    mu = (np.arange(1, n+1) - 0.5)/n
    return x - 1/(1 - c/(2*n) * (mu[:,None]*x / (mu[:,None] + mu)).sum(axis=1))

