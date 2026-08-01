
def F4_powell(x):
    A = 1e4
    return [A*x[0]*x[1] - 1, np.exp(-x[0]) + np.exp(-x[1]) - (1 + 1/A)]

