
def sph_legendre_p_0_0(theta):
    fac = sph_legendre_factor(0, 0)

    return np.full_like(theta, fac)

