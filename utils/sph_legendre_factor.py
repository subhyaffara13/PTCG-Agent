
def sph_legendre_factor(n, m):
    return assoc_legendre_factor(n, m, norm=True) / np.sqrt(2 * np.pi)

