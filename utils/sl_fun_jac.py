
def sl_fun_jac(x, y, p):
    n, m = y.shape
    df_dy = np.empty((n, 2, m))
    df_dy[0, 0] = 0
    df_dy[0, 1] = 1
    df_dy[1, 0] = -p[0]**2
    df_dy[1, 1] = 0

    df_dp = np.empty((n, 1, m))
    df_dp[0, 0] = 0
    df_dp[1, 0] = -2 * p[0] * y[0]

    return df_dy, df_dp

