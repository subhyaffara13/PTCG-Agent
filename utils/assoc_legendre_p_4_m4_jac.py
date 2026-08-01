
def assoc_legendre_p_4_m4_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, -4, norm)

    return fac * (z * z - 1) * z / 96

