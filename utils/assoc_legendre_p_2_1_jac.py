
def assoc_legendre_p_2_1_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(2, 1, norm)

    return (3 * fac * (2 * z * z - 1) *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut))

