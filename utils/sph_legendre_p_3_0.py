
def sph_legendre_p_3_0(theta):
    fac = sph_legendre_factor(3, 0)

    return (fac * (5 * np.square(np.cos(theta)) - 3) *
        np.cos(theta) / 2)

