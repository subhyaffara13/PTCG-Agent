
def test_orcsd_uncsd(dtype_):
    m, p, q = 250, 80, 170

    pfx = 'or' if dtype_ in REAL_DTYPES else 'un'
    X = ortho_group.rvs(m) if pfx == 'or' else unitary_group.rvs(m)

    drv, dlw = get_lapack_funcs((pfx + 'csd', pfx + 'csd_lwork'), dtype=dtype_)
    lwval = _compute_lwork(dlw, m, p, q)
    lwvals = {'lwork': lwval} if pfx == 'or' else dict(zip(['lwork',
                                                            'lrwork'], lwval))

    cs11, cs12, cs21, cs22, theta, u1, u2, v1t, v2t, info =\
        drv(X[:p, :q], X[:p, q:], X[p:, :q], X[p:, q:], **lwvals)

    assert info == 0

    U = block_diag(u1, u2)
    VH = block_diag(v1t, v2t)
    r = min(min(p, q), min(m-p, m-q))
    n11 = min(p, q) - r
    n12 = min(p, m-q) - r
    n21 = min(m-p, q) - r
    n22 = min(m-p, m-q) - r

    S = np.zeros((m, m), dtype=dtype_)
    one = dtype_(1.)
    for i in range(n11):
        S[i, i] = one
    for i in range(n22):
        S[p+i, q+i] = one
    for i in range(n12):
        S[i+n11+r, i+n11+r+n21+n22+r] = -one
    for i in range(n21):
        S[p+n22+r+i, n11+r+i] = one

    for i in range(r):
        S[i+n11, i+n11] = np.cos(theta[i])
        S[p+n22+i, i+r+n21+n22] = np.cos(theta[i])

        S[i+n11, i+n11+n21+n22+r] = -np.sin(theta[i])
        S[p+n22+i, i+n11] = np.sin(theta[i])

    Xc = U @ S @ VH
    assert_allclose(X, Xc, rtol=0., atol=1e4*np.finfo(dtype_).eps)

