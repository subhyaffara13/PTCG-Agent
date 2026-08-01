
def assoc_legendre_p_2_0(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(2, 0, norm)

    return fac * (3 * z * z - 1) / 2

