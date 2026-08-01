
def sph_legendre_p_3_1_jac(theta):
    fac = sph_legendre_factor(3, 1)

    return (3 * fac * (11 - 15 * np.square(np.cos(theta))) * np.cos(theta) *
        (2 * np.heaviside(np.sin(theta), 1) - 1) / 2)

