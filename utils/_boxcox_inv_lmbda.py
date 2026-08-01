
def _boxcox_inv_lmbda(x, y):
    # compute lmbda given x and y for Box-Cox transformation
    num = special.lambertw(-(x ** (-1 / y)) * np.log(x) / y, k=-1)
    return np.real(-num / np.log(x) - 1 / y)

