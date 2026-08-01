
def assoc_legendre_p_3_3_jac(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(3, 3, norm)

    return (45 * branch_cut_sign * fac * (1 - z * z) * z *
        assoc_legendre_p_1_1_jac_div_z(z, branch_cut=branch_cut))

