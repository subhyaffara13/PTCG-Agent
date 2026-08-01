
def assoc_legendre_p_2_0_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(2, 0, norm)

    return 3 * fac * z

