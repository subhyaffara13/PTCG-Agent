
def basic_1d_integrand_exact(n, xp):
    # Exact only for integration over interval [0, 2].
    return xp.reshape(2**(n+1)/(n+1), (-1, 1))

