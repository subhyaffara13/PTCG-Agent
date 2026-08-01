
def assoc_legendre_p_4_2(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(4, 2, norm)

    return 15 * branch_cut_sign * fac * ((8 - 7 * z * z) * z * z - 1) / 2

