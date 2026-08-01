
def assoc_legendre_p_4_3(z, *, branch_cut=2, norm=False):
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(4, 3, norm)

    return (105 * branch_cut_sign * fac * (1 - z * z) * z *
        assoc_legendre_p_1_1(z, branch_cut=branch_cut))

