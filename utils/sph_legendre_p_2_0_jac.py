
def sph_legendre_p_2_0_jac(theta):
    fac = sph_legendre_factor(2, 0)

    return -3 * fac * np.cos(theta) * np.sin(theta)

