
def assoc_legendre_p_4_1_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, 1, norm)

    return (5 * fac * ((28 * z * z - 27) * z * z + 3) *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut) / 2)

