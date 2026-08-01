
def assoc_legendre_p_0_0(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(0, 0, norm)

    return np.full_like(z, fac)

