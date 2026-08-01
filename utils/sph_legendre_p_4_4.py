
def sph_legendre_p_4_4(theta):
    fac = sph_legendre_factor(4, 4)

    return 105 * fac * np.square(np.square(np.cos(theta)) - 1)

