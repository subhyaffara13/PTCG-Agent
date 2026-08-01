
def aps13_f(x):
    r"""Function with *all* derivatives 0 at the root"""
    if x == 0:
        return 0
    # x2 = 1.0/x**2
    # if x2 > 708:
    #     return 0
    y = 1 / x**2
    if y > _MAX_EXPABLE:
        return 0
    return x / np.exp(y)

