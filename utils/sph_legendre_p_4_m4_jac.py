
def sph_legendre_p_4_m4_jac(theta):
    fac = sph_legendre_factor(4, -4)

    return (-fac * (np.square(np.cos(theta)) - 1) *
        np.sin(theta) * np.cos(theta) / 96)

