
def assoc_legendre_p_1_1_jac_div_z(z, branch_cut=2):
    branch_sign = np.where(branch_cut == 3, np.where(np.signbit(np.real(z)), 1, -1), -1)

    out11_div_z = (-branch_sign /
        np.sqrt(np.where(branch_cut == 3, z * z - 1, 1 - z * z)))

    return out11_div_z

