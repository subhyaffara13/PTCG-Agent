
def sph_legendre_p_4_2_jac(theta):
    fac = sph_legendre_factor(4, 2)

    return (30 * fac * (7 * np.square(np.cos(theta)) - 4) *
        np.sin(theta) * np.cos(theta))

