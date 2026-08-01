
def sph_legendre_p_4_0_jac(theta):
    fac = sph_legendre_factor(4, 0)

    return (-5 * fac * (7 * np.square(np.cos(theta)) - 3) *
        np.sin(theta) * np.cos(theta) / 2)

