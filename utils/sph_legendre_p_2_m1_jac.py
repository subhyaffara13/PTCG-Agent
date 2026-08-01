
def sph_legendre_p_2_m1_jac(theta):
    fac = sph_legendre_factor(2, -1)

    return (-fac * (-np.square(np.cos(theta)) *
        (2 * np.heaviside(np.sin(theta), 1) - 1) +
        np.abs(np.sin(theta)) * np.sin(theta)) / 2)

