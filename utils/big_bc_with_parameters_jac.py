
def big_bc_with_parameters_jac(ya, yb, p):
    # big version of sl_bc_jac, with two parameters
    n = ya.shape[0]
    dbc_dya = np.zeros((n + 2, n))
    dbc_dyb = np.zeros((n + 2, n))

    dbc_dya[range(n // 2), range(0, n, 2)] = 1
    dbc_dyb[range(n // 2, n), range(0, n, 2)] = 1

    dbc_dp = np.zeros((n + 2, 2))
    dbc_dp[n, 0] = -1
    dbc_dya[n, 1] = 1
    dbc_dp[n + 1, 1] = -1
    dbc_dya[n + 1, 3] = 1

    return dbc_dya, dbc_dyb, dbc_dp

