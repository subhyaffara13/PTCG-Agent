
def sph_legendre_p_3_m3(theta):
    fac = sph_legendre_factor(3, -3)

    return fac * np.power(np.abs(np.sin(theta)), 3) / 48

