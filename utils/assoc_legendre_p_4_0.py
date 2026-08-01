
def assoc_legendre_p_4_0(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, 0, norm)

    return fac * ((35 * z * z - 30) * z * z + 3) / 8

