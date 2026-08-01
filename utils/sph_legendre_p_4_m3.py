
def sph_legendre_p_4_m3(theta):
    fac = sph_legendre_factor(4, -3)

    return (fac * np.power(np.abs(np.sin(theta)), 3) *
        np.cos(theta) / 48)

