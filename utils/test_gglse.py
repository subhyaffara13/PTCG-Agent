
def test_gglse():
    # Example data taken from NAG manual
    for ind, dtype in enumerate(DTYPES):
        # DTYPES = <s,d,c,z> gglse
        func, func_lwork = get_lapack_funcs(('gglse', 'gglse_lwork'),
                                            dtype=dtype)
        lwork = _compute_lwork(func_lwork, m=6, n=4, p=2)
        # For <s,d>gglse
        if ind < 2:
            a = np.array([[-0.57, -1.28, -0.39, 0.25],
                          [-1.93, 1.08, -0.31, -2.14],
                          [2.30, 0.24, 0.40, -0.35],
                          [-1.93, 0.64, -0.66, 0.08],
                          [0.15, 0.30, 0.15, -2.13],
                          [-0.02, 1.03, -1.43, 0.50]], dtype=dtype)
            c = np.array([-1.50, -2.14, 1.23, -0.54, -1.68, 0.82], dtype=dtype)
            d = np.array([0., 0.], dtype=dtype)
        # For <s,d>gglse
        else:
            a = np.array([[0.96-0.81j, -0.03+0.96j, -0.91+2.06j, -0.05+0.41j],
                          [-0.98+1.98j, -1.20+0.19j, -0.66+0.42j, -0.81+0.56j],
                          [0.62-0.46j, 1.01+0.02j, 0.63-0.17j, -1.11+0.60j],
                          [0.37+0.38j, 0.19-0.54j, -0.98-0.36j, 0.22-0.20j],
                          [0.83+0.51j, 0.20+0.01j, -0.17-0.46j, 1.47+1.59j],
                          [1.08-0.28j, 0.20-0.12j, -0.07+1.23j, 0.26+0.26j]])
            c = np.array([[-2.54+0.09j],
                          [1.65-2.26j],
                          [-2.11-3.96j],
                          [1.82+3.30j],
                          [-6.41+3.77j],
                          [2.07+0.66j]])
            d = np.zeros(2, dtype=dtype)

        b = np.array([[1., 0., -1., 0.], [0., 1., 0., -1.]], dtype=dtype)

        _, _, _, result, _ = func(a, b, c, d, lwork=lwork)
        if ind < 2:
            expected = np.array([0.48904455,
                                 0.99754786,
                                 0.48904455,
                                 0.99754786])
        else:
            expected = np.array([1.08742917-1.96205783j,
                                 -0.74093902+3.72973919j,
                                 1.08742917-1.96205759j,
                                 -0.74093896+3.72973895j])
        assert_array_almost_equal(result, expected, decimal=4)

