
def sph_legendre_p_4_m2_jac(theta):
    fac = sph_legendre_factor(4, -2)

    return (fac * (7 * np.square(np.cos(theta)) - 4) * np.sin(theta) *
        np.cos(theta) / 12)

