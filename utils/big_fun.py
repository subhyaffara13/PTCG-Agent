
def big_fun(x, y):
    f = np.zeros_like(y)
    f[::2] = y[1::2]
    return f

