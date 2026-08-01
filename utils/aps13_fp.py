
def aps13_fp(x):
    if x == 0:
        return 0
    y = 1 / x**2
    if y > _MAX_EXPABLE:
        return 0
    return (1 + 2 / x**2) / np.exp(y)

