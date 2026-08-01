
def sph_legendre_p_4_1(theta):
    fac = sph_legendre_factor(4, 1)

    return (-5 * fac * (7 * np.square(np.cos(theta)) - 3) *
        np.cos(theta) * np.abs(np.sin(theta)) / 2)

