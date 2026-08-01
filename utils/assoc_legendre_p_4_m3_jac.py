
def assoc_legendre_p_4_m3_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, -3, norm)

    return (fac * ((4 * z * z - 5) * z * z + 1) *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut) / 48)

