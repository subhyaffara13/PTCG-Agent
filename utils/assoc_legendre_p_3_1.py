
def assoc_legendre_p_3_1(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(3, 1, norm)

    return (3 * fac * (5 * z * z - 1) *
        assoc_legendre_p_1_1(z, branch_cut=branch_cut) / 2)

