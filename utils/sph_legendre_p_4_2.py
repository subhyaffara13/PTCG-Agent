
def sph_legendre_p_4_2(theta):
    fac = sph_legendre_factor(4, 2)

    return (-15 * fac * (7 * np.square(np.cos(theta)) - 1) *
        (np.square(np.cos(theta)) - 1) / 2)

