
def sph_legendre_p_3_2_jac(theta):
    fac = sph_legendre_factor(3, 2)

    return 15 * fac * (3 * np.square(np.cos(theta)) - 1) * np.sin(theta)

