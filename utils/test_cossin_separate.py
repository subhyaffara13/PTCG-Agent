
def test_cossin_separate(dtype_):
    rng = default_rng(1708093590167096)
    m, p, q = 98, 37, 61

    pfx = 'or' if dtype_ in REAL_DTYPES else 'un'
    X = (ortho_group.rvs(m, random_state=rng) if pfx == 'or'
         else unitary_group.rvs(m, random_state=rng))
    X = np.array(X, dtype=dtype_)

    drv, dlw = get_lapack_funcs((pfx + 'csd', pfx + 'csd_lwork'), [X])
    lwval = _compute_lwork(dlw, m, p, q)
    lwvals = {'lwork': lwval} if pfx == 'or' else dict(zip(['lwork',
                                                            'lrwork'],
                                                           lwval))

    *_, theta, u1, u2, v1t, v2t, _ = \
        drv(X[:p, :q], X[:p, q:], X[p:, :q], X[p:, q:], **lwvals)

    (u1_2, u2_2), theta2, (v1t_2, v2t_2) = cossin(X, p, q, separate=True)

    assert_allclose(u1_2, u1, rtol=0., atol=10*np.finfo(dtype_).eps)
    assert_allclose(u2_2, u2, rtol=0., atol=10*np.finfo(dtype_).eps)
    assert_allclose(v1t_2, v1t, rtol=0., atol=10*np.finfo(dtype_).eps)
    assert_allclose(v2t_2, v2t, rtol=0., atol=10*np.finfo(dtype_).eps)
    assert_allclose(theta2, theta, rtol=0., atol=10*np.finfo(dtype_).eps)

