
def test_lantr(norm, uplo, m, n, diag, dtype):
    rng = np.random.default_rng(98426598246982456)
    A = rng.random(size=(m, n)).astype(dtype)
    lantr, lange = get_lapack_funcs(('lantr', 'lange'), (A,))
    res = lantr(norm, A, uplo=uplo, diag=diag)

    # now modify the matrix according to assumptions made by `lantr`
    A = np.triu(A) if uplo == 'U' else np.tril(A)
    if diag == 'U':
        i = np.arange(min(m, n))
        A[i, i] = 1
    ref = lange(norm, A)

    assert_allclose(res, ref, rtol=2e-6)

