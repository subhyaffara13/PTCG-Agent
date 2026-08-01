
def assoc_legendre_p_4_0_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, 0, norm)

    return 5 * fac * (7 * z * z - 3) * z / 2

