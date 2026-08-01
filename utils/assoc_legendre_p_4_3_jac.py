
def assoc_legendre_p_4_3_jac(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(4, 3, norm)

    return (105 * branch_cut_sign * fac * ((5 - 4 * z * z) * z * z - 1) *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut))

