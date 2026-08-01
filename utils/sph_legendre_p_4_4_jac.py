
def sph_legendre_p_4_4_jac(theta):
    fac = sph_legendre_factor(4, 4)

    return (-420 * fac * (np.square(np.cos(theta)) - 1) *
        np.sin(theta) * np.cos(theta))

