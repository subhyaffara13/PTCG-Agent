
def sph_legendre_p_2_1(theta):
    fac = sph_legendre_factor(2, 1)

    return -3 * fac * np.abs(np.sin(theta)) * np.cos(theta)

