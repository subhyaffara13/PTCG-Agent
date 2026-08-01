
def sph_legendre_p_3_2(theta):
    fac = sph_legendre_factor(3, 2)

    return (-15 * fac * (np.square(np.cos(theta)) - 1) *
        np.cos(theta))

