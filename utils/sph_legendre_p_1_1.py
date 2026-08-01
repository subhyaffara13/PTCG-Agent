
def sph_legendre_p_1_1(theta):
    fac = sph_legendre_factor(1, 1)

    return -fac * np.abs(np.sin(theta))

