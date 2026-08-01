
def basic_nd_integrand(x, n, xp):
    return xp.reshape(xp.sum(x, axis=-1), (-1, 1))**xp.reshape(n, (1, -1))

