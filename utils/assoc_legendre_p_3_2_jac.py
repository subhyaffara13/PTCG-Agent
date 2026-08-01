
def assoc_legendre_p_3_2_jac(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(3, 2, norm)

    return 15 * branch_cut_sign * fac * (1 - 3 * z * z)

