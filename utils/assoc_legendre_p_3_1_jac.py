
def assoc_legendre_p_3_1_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(3, 1, norm)

    return (3 * fac * (15 * z * z - 11) * z *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut) / 2)

