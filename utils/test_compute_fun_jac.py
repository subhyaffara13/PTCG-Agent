
def test_compute_fun_jac():
    x = np.linspace(0, 1, 5)
    y = np.empty((2, x.shape[0]))
    y[0] = 0.01
    y[1] = 0.02
    p = np.array([])
    df_dy, df_dp = estimate_fun_jac(lambda x, y, p: exp_fun(x, y), x, y, p)
    df_dy_an = exp_fun_jac(x, y)
    assert_allclose(df_dy, df_dy_an)
    assert_(df_dp is None)

    x = np.linspace(0, np.pi, 5)
    y = np.empty((2, x.shape[0]))
    y[0] = np.sin(x)
    y[1] = np.cos(x)
    p = np.array([1.0])
    df_dy, df_dp = estimate_fun_jac(sl_fun, x, y, p)
    df_dy_an, df_dp_an = sl_fun_jac(x, y, p)
    assert_allclose(df_dy, df_dy_an)
    assert_allclose(df_dp, df_dp_an)

    x = np.linspace(0, 1, 10)
    y = np.empty((2, x.shape[0]))
    y[0] = (3/4)**0.5
    y[1] = 1e-4
    p = np.array([])
    df_dy, df_dp = estimate_fun_jac(lambda x, y, p: emden_fun(x, y), x, y, p)
    df_dy_an = emden_fun_jac(x, y)
    assert_allclose(df_dy, df_dy_an)
    assert_(df_dp is None)

