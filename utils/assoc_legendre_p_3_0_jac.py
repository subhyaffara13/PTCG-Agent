
def assoc_legendre_p_3_0_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(3, 0, norm)

    return 3 * fac * (5 * z * z - 1) / 2

