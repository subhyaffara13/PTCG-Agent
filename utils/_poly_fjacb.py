
def _poly_fjacb(B, x, powers):
    res = np.concatenate((np.ones(x.shape[-1], float),
                          np.power(x, powers).flat))
    return res.reshape((B.shape[-1], x.shape[-1]))

