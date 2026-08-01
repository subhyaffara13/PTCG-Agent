
def assoc_legendre_p_1_0_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(1, 0, norm)

    return np.full_like(z, fac)

