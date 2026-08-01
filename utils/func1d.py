
def func1d(x):
    f = cos(14.5 * x - 0.3) + (x + 0.2) * x
    df = np.array(-14.5 * sin(14.5 * x - 0.3) + 2. * x + 0.2)
    return f, df

