
def sl_bc_jac(ya, yb, p):
    dbc_dya = np.zeros((3, 2))
    dbc_dya[0, 0] = 1
    dbc_dya[2, 1] = 1

    dbc_dyb = np.zeros((3, 2))
    dbc_dyb[1, 0] = 1

    dbc_dp = np.zeros((3, 1))
    dbc_dp[2, 0] = -1

    return dbc_dya, dbc_dyb, dbc_dp

