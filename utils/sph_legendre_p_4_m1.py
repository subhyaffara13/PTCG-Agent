
def sph_legendre_p_4_m1(theta):
    fac = sph_legendre_factor(4, -1)

    return (fac * (7 * np.square(np.cos(theta)) - 3) *
        np.cos(theta) * np.abs(np.sin(theta)) / 8)

