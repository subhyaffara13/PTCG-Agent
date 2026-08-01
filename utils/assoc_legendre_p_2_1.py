
def assoc_legendre_p_2_1(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(2, 1, norm)

    return (3 * fac * z *
        assoc_legendre_p_1_1(z, branch_cut=branch_cut))

