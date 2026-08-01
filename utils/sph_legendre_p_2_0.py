
def sph_legendre_p_2_0(theta):
    fac = sph_legendre_factor(2, 0)

    return fac * (3 * np.square(np.cos(theta)) - 1) / 2

