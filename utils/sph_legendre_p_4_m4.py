
def sph_legendre_p_4_m4(theta):
    fac = sph_legendre_factor(4, -4)

    return fac * np.square(np.square(np.cos(theta)) - 1) / 384

