
def test_gtcon(dtype, norm, n):
    rng = np.random.default_rng(23498324)

    d = rng.random(n) + rng.random(n)*1j
    dl = rng.random(n - 1) + rng.random(n - 1)*1j
    du = rng.random(n - 1) + rng.random(n - 1)*1j
    A = np.diag(d) + np.diag(dl, -1) + np.diag(du, 1)
    if np.issubdtype(dtype, np.floating):
        A, d, dl, du = A.real, d.real, dl.real, du.real
    A, d, dl, du = A.astype(dtype), d.astype(dtype), dl.astype(dtype), du.astype(dtype)

    anorm = np.linalg.norm(A, ord=np.inf if norm == 'I' else 1)

    gttrf, gtcon = get_lapack_funcs(('gttrf', 'gtcon'), (A,))
    dl, d, du, du2, ipiv, info = gttrf(dl, d, du)
    res, _ = gtcon(dl, d, du, du2, ipiv, anorm, norm=norm)

    gecon, getrf = get_lapack_funcs(('gecon', 'getrf'), (A,))
    lu, ipvt, info = getrf(A)
    ref, _ = gecon(lu, anorm, norm=norm)

    rtol = np.finfo(dtype).eps**0.75
    assert_allclose(res, ref, rtol=rtol)

