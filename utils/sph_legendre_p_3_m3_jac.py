
def sph_legendre_p_3_m3_jac(theta):
    fac = sph_legendre_factor(3, -3)

    return fac * np.abs(np.sin(theta)) * np.sin(theta) * np.cos(theta) / 16

