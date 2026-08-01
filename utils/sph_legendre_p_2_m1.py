
def sph_legendre_p_2_m1(theta):
    fac = sph_legendre_factor(2, -1)

    return fac * np.cos(theta) * np.abs(np.sin(theta)) / 2

