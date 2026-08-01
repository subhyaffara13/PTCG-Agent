
def _poly_fcn(B, x, powers):
    a, b = B[0], B[1:]
    b = b.reshape((b.shape[0], 1))

    return a + np.sum(b * np.power(x, powers), axis=0)

