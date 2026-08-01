
def sph_legendre_p_2_2(theta):
    fac = sph_legendre_factor(2, 2)

    return 3 * fac * (1 - np.square(np.cos(theta)))

