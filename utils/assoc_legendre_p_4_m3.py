
def assoc_legendre_p_4_m3(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, -3, norm)

    return (fac * (z * z - 1) * z *
        assoc_legendre_p_1_1(z, branch_cut=branch_cut) / 48)

