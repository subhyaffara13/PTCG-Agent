
def assoc_legendre_p_1_1(z, *, branch_cut=2, norm=False):
    branch_sign = np.where(branch_cut == 3, np.where(np.signbit(np.real(z)), 1, -1), -1)
    branch_cut_sign = np.where(branch_cut == 3, -1, 1)
    fac = assoc_legendre_factor(1, 1, norm)

    w = np.sqrt(np.where(branch_cut == 3, z * z - 1, 1 - z * z))

    return branch_cut_sign * branch_sign * fac * w

