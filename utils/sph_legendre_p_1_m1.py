
def sph_legendre_p_1_m1(theta):
    fac = sph_legendre_factor(1, -1)

    return fac * np.abs(np.sin(theta)) / 2

