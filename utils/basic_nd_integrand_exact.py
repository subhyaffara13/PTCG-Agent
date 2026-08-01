
def basic_nd_integrand_exact(n, xp):
    # Exact only for integration over interval [0, 2].
    return (-2**(3+n) + 4**(2+n))/((1+n)*(2+n))

