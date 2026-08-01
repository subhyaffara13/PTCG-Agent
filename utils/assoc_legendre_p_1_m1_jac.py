
def assoc_legendre_p_1_m1_jac(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(1, -1, norm)

    return (-branch_cut_sign * fac * z *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut) / 2)

