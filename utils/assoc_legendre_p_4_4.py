
def assoc_legendre_p_4_4(z, *, branch_cut=2, norm=False):
    fac = assoc_legendre_factor(4, 4, norm)

    return 105 * fac * np.square(z * z - 1)

