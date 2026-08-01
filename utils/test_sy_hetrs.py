
def test_sy_hetrs(mtype, dtype, lower):
    if mtype == 'he' and dtype in REAL_DTYPES:
        pytest.skip("hetrs not for real dtypes.")
    rng = np.random.default_rng(1723059677121834)
    n, nrhs = 20, 5
    if dtype in COMPLEX_DTYPES:
        A = (rng.uniform(size=(n, n)) + rng.uniform(size=(n, n))*1j).astype(dtype)
    else:
        A = rng.uniform(size=(n, n)).astype(dtype)

    A = A + A.T if mtype == 'sy' else A + A.conj().T
    b = rng.uniform(size=(n, nrhs)).astype(dtype)
    names = f'{mtype}trf', f'{mtype}trf_lwork', f'{mtype}trs'
    trf, trf_lwork, trs = get_lapack_funcs(names, dtype=dtype)
    lwork = trf_lwork(n, lower=lower)
    ldu, ipiv, info = trf(A, lwork=lwork, lower=lower)
    assert info == 0
    x, info = trs(a=ldu, ipiv=ipiv, b=b, lower=lower)
    assert info == 0
    eps = np.finfo(dtype).eps
    assert_allclose(A@x, b, atol=100*n*eps)

