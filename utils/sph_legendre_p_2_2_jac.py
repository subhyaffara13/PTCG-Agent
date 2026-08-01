
def sph_legendre_p_2_2_jac(theta):
    fac = sph_legendre_factor(2, 2)

    return 6 * fac * np.sin(theta) * np.cos(theta)

