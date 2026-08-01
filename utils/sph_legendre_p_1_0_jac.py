
def sph_legendre_p_1_0_jac(theta):
    fac = sph_legendre_factor(1, 0)

    return -fac * np.sin(theta)

