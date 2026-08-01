
def sph_legendre_p_3_m2(theta):
    fac = sph_legendre_factor(3, -2)

    return (-fac * (np.square(np.cos(theta)) - 1) *
        np.cos(theta) / 8)

