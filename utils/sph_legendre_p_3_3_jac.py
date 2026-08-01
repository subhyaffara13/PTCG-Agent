
def sph_legendre_p_3_3_jac(theta):
    fac = sph_legendre_factor(3, 3)

    return -45 * fac * np.abs(np.sin(theta)) * np.sin(theta) * np.cos(theta)

