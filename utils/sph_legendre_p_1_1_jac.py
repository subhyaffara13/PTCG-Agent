
def sph_legendre_p_1_1_jac(theta):
    fac = sph_legendre_factor(1, 1)

    return -fac * np.cos(theta) * (2 * np.heaviside(np.sin(theta), 1) - 1)

