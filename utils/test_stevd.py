
def test_stevd(dtype, compute_v):
    rng = np.random.default_rng(266474747488348746)
    n = 10
    d = rng.random(n, dtype=dtype)
    e = rng.random(n - 1, dtype=dtype)
    A = np.diag(e, -1) + np.diag(d) + np.diag(e, 1)
    ref = np.linalg.eigvalsh(A)

    stevd = get_lapack_funcs('stevd')
    U, V, info = stevd(d, e, compute_v=compute_v)
    assert info == 0
    assert_allclose(np.sort(U), np.sort(ref))
    if compute_v:
        eps = np.finfo(dtype).eps
        assert_allclose(V @ np.diag(U) @ V.T, A, atol=eps**0.8)

