
def sph_legendre_p_3_3(theta):
    fac = sph_legendre_factor(3, 3)

    return -15 * fac * np.power(np.abs(np.sin(theta)), 3)

