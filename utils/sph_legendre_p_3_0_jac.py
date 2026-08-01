
def sph_legendre_p_3_0_jac(theta):
    fac = sph_legendre_factor(3, 0)

    return 3 * fac * (1 - 5 * np.square(np.cos(theta))) * np.sin(theta) / 2

