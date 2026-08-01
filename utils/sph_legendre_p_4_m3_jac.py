
def sph_legendre_p_4_m3_jac(theta):
    fac = sph_legendre_factor(4, -3)

    return (fac * (4 * np.square(np.cos(theta)) - 1) *
        np.abs(np.sin(theta)) * np.sin(theta) / 48)

