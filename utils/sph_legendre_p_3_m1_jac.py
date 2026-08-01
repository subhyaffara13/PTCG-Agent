
def sph_legendre_p_3_m1_jac(theta):
    fac = sph_legendre_factor(3, -1)

    return (-fac * (11 - 15 * np.square(np.cos(theta))) *
        np.cos(theta) *
        (2 * np.heaviside(np.sin(theta), 1) - 1) / 8)

