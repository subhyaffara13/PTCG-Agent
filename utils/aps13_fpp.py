
def aps13_fpp(x):
    if x == 0:
        return 0
    y = 1 / x**2
    if y > _MAX_EXPABLE:
        return 0
    return 2 * (2 - x**2) / x**5 / np.exp(y)

