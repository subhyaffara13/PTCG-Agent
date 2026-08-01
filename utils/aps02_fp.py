
def aps02_fp(x):
    ii = np.arange(1, 21)
    return 6 * np.sum((2 * ii - 5)**2 / (x - ii**2)**4)

