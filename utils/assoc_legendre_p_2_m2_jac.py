
def assoc_legendre_p_2_m2_jac(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(2, -2, norm)

    return -branch_cut_sign * fac * z / 4

