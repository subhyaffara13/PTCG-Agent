
def sph_legendre_p_2_m2(theta):
    fac = sph_legendre_factor(2, -2)

    return fac * (1 - np.square(np.cos(theta))) / 8

