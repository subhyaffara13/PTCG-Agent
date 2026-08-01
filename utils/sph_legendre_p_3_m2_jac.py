
def sph_legendre_p_3_m2_jac(theta):
    fac = sph_legendre_factor(3, -2)

    return fac * (3 * np.square(np.cos(theta)) - 1) * np.sin(theta) / 8

