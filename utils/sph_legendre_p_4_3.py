
def sph_legendre_p_4_3(theta):
    fac = sph_legendre_factor(4, 3)

    return -105 * fac * np.power(np.abs(np.sin(theta)), 3) * np.cos(theta)

