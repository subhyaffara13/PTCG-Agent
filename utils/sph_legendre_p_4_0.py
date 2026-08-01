
def sph_legendre_p_4_0(theta):
    fac = sph_legendre_factor(4, 0)

    return (fac * (35 * np.square(np.square(np.cos(theta))) -
        30 * np.square(np.cos(theta)) + 3) / 8)

