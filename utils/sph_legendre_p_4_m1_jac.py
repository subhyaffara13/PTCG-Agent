
def sph_legendre_p_4_m1_jac(theta):
    fac = sph_legendre_factor(4, -1)

    return (-fac * (-3 + 27 * np.square(np.cos(theta)) -
        28 * np.square(np.square(np.cos(theta)))) *
        (2 * np.heaviside(np.sin(theta), 1) - 1) / 8)

