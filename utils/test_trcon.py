
def test_trcon(dtype, norm, uplo, diag, n):
    # Simple way to get deterministic (unlike `hash`) seed based on arguments
    seed = list(f"{dtype}{norm}{uplo}{diag}{n}".encode())
    rng = np.random.default_rng(seed)

    A = rng.random(size=(n, n)) + rng.random(size=(n, n))*1j
    # make the condition numbers more interesting
    offset = rng.permuted(np.logspace(0, rng.integers(0, 10), n))
    A += offset
    A = A.real if np.issubdtype(dtype, np.floating) else A
    A = np.triu(A) if uplo == 'U' else np.tril(A)
    if diag == 'U':
        A /= np.diag(A)[:, np.newaxis]
    A = A.astype(dtype)

    trcon = get_lapack_funcs('trcon', (A,))
    res, _ = trcon(A, norm=norm, uplo=uplo, diag=diag)

    if norm == 'I':
        norm_A = np.linalg.norm(A, ord=np.inf)
        norm_inv_A = np.linalg.norm(np.linalg.inv(A), ord=np.inf)
        ref = 1 / (norm_A * norm_inv_A)
    else:
        anorm = np.linalg.norm(A, ord=1)
        gecon, getrf = get_lapack_funcs(('gecon', 'getrf'), (A,))
        lu, ipvt, info = getrf(A)
        ref, _ = gecon(lu, anorm, norm=norm)

    # This is an estimate of reciprocal condition number; we just need order of
    # magnitude. In testing, we observed that much smaller rtol is OK in almost
    # all cases... but sometimes it isn't.
    rtol = 1  # np.finfo(dtype).eps**0.75
    assert_allclose(res, ref, rtol=rtol)

