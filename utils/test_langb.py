
def test_langb(dtype, norm):
    rng = np.random.default_rng(17273783424)

    # A is of shape n x n with ku/kl super/sub-diagonals
    n, ku, kl = 10, 2, 2
    A = rng.random((n, n)) + rng.random((n, n))*1j
    if np.issubdtype(dtype, np.floating):
        A = A.real
    A = A.astype(dtype)
    A[np.triu_indices(n, ku + 1)] = 0
    A[np.tril_indices(n, -kl - 1)] = 0
    ab = _to_banded(kl, ku, A)

    langb, lange = get_lapack_funcs(('langb', 'lange'), (A,))
    ref = lange(norm, A)
    res = langb(norm, kl, ku, ab)
    assert_allclose(res, ref, rtol=2e-6)

