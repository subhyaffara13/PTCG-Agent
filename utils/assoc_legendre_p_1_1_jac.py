
def assoc_legendre_p_1_1_jac(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(1, 1, norm)

    return (fac * z *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut))

