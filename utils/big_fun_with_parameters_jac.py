
def big_fun_with_parameters_jac(x, y, p):
    # big version of sl_fun_jac, with two parameters
    n, m = y.shape
    df_dy = np.zeros((n, n, m))
    df_dy[range(0, n, 2), range(1, n, 2)] = 1
    df_dy[range(1, n, 4), range(0, n, 4)] = -p[0]**2
    df_dy[range(3, n, 4), range(2, n, 4)] = -p[1]**2

    df_dp = np.zeros((n, 2, m))
    df_dp[range(1, n, 4), 0] = -2 * p[0] * y[range(0, n, 4)]
    df_dp[range(3, n, 4), 1] = -2 * p[1] * y[range(2, n, 4)]

    return df_dy, df_dp

