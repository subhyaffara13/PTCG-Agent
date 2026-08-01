
def test_sy_he_tri(dtype, lower, mtype):
    if mtype == 'he' and dtype in REAL_DTYPES:
        pytest.skip("hetri not for real dtypes.")
    if sysconfig.get_platform() == 'win-arm64' and dtype in COMPLEX_DTYPES:
        pytest.skip("Test segfaulting on win-arm64 in CI, see gh-23133")

    rng = np.random.default_rng(1723059677121834)
    n = 20
    A = rng.random((n, n)) + rng.random((n, n))*1j
    if np.issubdtype(dtype, np.floating):
        A = A.real
    A = A.astype(dtype)
    A = A + A.T if mtype == 'sy' else A + A.conj().T
    names = f'{mtype}trf', f'{mtype}tri'
    trf, tri = get_lapack_funcs(names, dtype=dtype)
    ldu, ipiv, info = trf(A, lower=lower)
    assert info == 0
    A_inv, info = tri(a=ldu, ipiv=ipiv, lower=lower)
    assert info == 0
    eps = np.finfo(dtype).eps
    ref = np.linalg.inv(A)
    if lower:
        assert_allclose(np.tril(A_inv), np.tril(ref), atol=100*n*eps)
    else:
        assert_allclose(np.triu(A_inv), np.triu(ref), atol=100*n*eps)

