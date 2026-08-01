
def sph_legendre_p_2_m2_jac(theta):
    fac = sph_legendre_factor(2, -2)

    return fac * np.sin(theta) * np.cos(theta) / 4

