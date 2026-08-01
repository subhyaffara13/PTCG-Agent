
def assoc_legendre_p_3_m3_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(3, -3, norm)

    return (fac * (z * z - 1) * z *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut) / 16)

