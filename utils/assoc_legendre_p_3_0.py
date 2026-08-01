
def assoc_legendre_p_3_0(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(3, 0, norm)

    return fac * (5 * z * z - 3) * z / 2

