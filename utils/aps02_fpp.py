
def aps02_fpp(x):
    ii = np.arange(1, 21)
    return 24 * np.sum((2 * ii - 5)**2 / (x - ii**2)**5)

