
def test_tzrzf():
    """
    This test performs an RZ decomposition in which an m x n upper trapezoidal
    array M (m <= n) is factorized as M = [R 0] * Z where R is upper triangular
    and Z is unitary.
    """
    rng = np.random.RandomState(1234)
    m, n = 10, 15
    for ind, dtype in enumerate(DTYPES):
        tzrzf, tzrzf_lw = get_lapack_funcs(('tzrzf', 'tzrzf_lwork'),
                                           dtype=dtype)
        lwork = _compute_lwork(tzrzf_lw, m, n)

        if ind < 2:
            A = triu(rng.rand(m, n).astype(dtype))
        else:
            A = triu((rng.rand(m, n) + rng.rand(m, n)*1j).astype(dtype))

        # assert wrong shape arg, f2py returns generic error
        assert_raises(Exception, tzrzf, A.T)
        rz, tau, info = tzrzf(A, lwork=lwork)
        # Check success
        assert_(info == 0)

        # Get Z manually for comparison
        R = np.hstack((rz[:, :m], np.zeros((m, n-m), dtype=dtype)))
        V = np.hstack((np.eye(m, dtype=dtype), rz[:, m:]))
        Id = np.eye(n, dtype=dtype)
        ref = [Id-tau[x]*V[[x], :].T.dot(V[[x], :].conj()) for x in range(m)]
        Z = reduce(np.dot, ref)
        assert_allclose(R.dot(Z) - A, zeros_like(A, dtype=dtype),
                        atol=10*np.spacing(dtype(1.0).real), rtol=0.)

