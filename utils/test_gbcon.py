
def test_gbcon(dtype, norm):
    rng = np.random.default_rng(17273783424)

    # A is of shape n x n with ku/kl super/sub-diagonals
    n, ku, kl = 10, 2, 2
    A = rng.random((n, n)) + rng.random((n, n))*1j
    # make the condition numbers more interesting
    offset = rng.permuted(np.logspace(0, rng.integers(0, 10), n))
    A += offset
    if np.issubdtype(dtype, np.floating):
        A = A.real
    A = A.astype(dtype)
    A[np.triu_indices(n, ku + 1)] = 0
    A[np.tril_indices(n, -kl - 1)] = 0

    # construct banded form
    tmp = _to_banded(kl, ku, A)
    # add rows required by ?gbtrf
    LDAB = 2*kl + ku + 1
    ab = np.zeros((LDAB, n), dtype=dtype)
    ab[kl:, :] = tmp

    anorm = np.linalg.norm(A, ord=np.inf if norm == 'I' else 1)
    gbcon, gbtrf = get_lapack_funcs(("gbcon", "gbtrf"), (ab,))
    lu_band, ipiv, _ = gbtrf(ab, kl, ku)
    res = gbcon(norm=norm, kl=kl, ku=ku, ab=lu_band, ipiv=ipiv,
                anorm=anorm)[0]

    gecon, getrf = get_lapack_funcs(('gecon', 'getrf'), (A,))
    lu = getrf(A)[0]
    ref = gecon(lu, anorm, norm=norm)[0]
    # This is an estimate of reciprocal condition number; we just need order of
    # magnitude.
    assert_allclose(res, ref, rtol=1)

