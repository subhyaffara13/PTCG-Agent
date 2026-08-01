
def sph_legendre_p_3_1(theta):
    fac = sph_legendre_factor(3, 1)

    return (-3 * fac * (5 * np.square(np.cos(theta)) - 1) *
        np.abs(np.sin(theta)) / 2)

