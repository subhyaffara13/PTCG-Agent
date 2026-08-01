
def assoc_legendre_p_4_1(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, 1, norm)

    return (5 * fac * (7 * z * z - 3) * z *
       assoc_legendre_p_1_1(z, branch_cut=branch_cut) / 2)

