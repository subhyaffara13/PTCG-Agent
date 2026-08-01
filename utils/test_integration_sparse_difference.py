
def test_integration_sparse_difference():
    n = 200
    t_span = [0, 20]
    y0 = np.zeros(2 * n)
    y0[1::2] = 1
    sparsity = medazko_sparsity(n)

    for method in ['BDF', 'Radau']:
        res = solve_ivp(fun_medazko, t_span, y0, method=method,
                        jac_sparsity=sparsity)

        assert_equal(res.t[0], t_span[0])
        assert_(res.t_events is None)
        assert_(res.y_events is None)
        assert_(res.success)
        assert_equal(res.status, 0)

        assert_allclose(res.y[78, -1], 0.233994e-3, rtol=1e-2)
        assert_allclose(res.y[79, -1], 0, atol=1e-3)
        assert_allclose(res.y[148, -1], 0.359561e-3, rtol=1e-2)
        assert_allclose(res.y[149, -1], 0, atol=1e-3)
        assert_allclose(res.y[198, -1], 0.117374129e-3, rtol=1e-2)
        assert_allclose(res.y[199, -1], 0.6190807e-5, atol=1e-3)
        assert_allclose(res.y[238, -1], 0, atol=1e-3)
        assert_allclose(res.y[239, -1], 0.9999997, rtol=1e-2)

