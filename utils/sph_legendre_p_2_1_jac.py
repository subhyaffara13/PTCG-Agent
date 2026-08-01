
def sph_legendre_p_2_1_jac(theta):
    fac = sph_legendre_factor(2, 1)

    return (3 * fac * (-np.square(np.cos(theta)) *
        (2 * np.heaviside(np.sin(theta), 1) - 1) +
        np.abs(np.sin(theta)) * np.sin(theta)))

