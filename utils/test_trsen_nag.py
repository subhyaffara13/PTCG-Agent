
def test_trsen_NAG(t, q, select, expect, expect_s, expect_sep):
    """
    This test implements the example found in the NAG manual,
    f08qgc, f08quc.
    """
    # NAG manual provides accuracy up to 4 and 2 decimals
    atol = 1e-4
    atol2 = 1e-2
    trsen, trsen_lwork = get_lapack_funcs(
        ('trsen', 'trsen_lwork'), dtype=t.dtype)

    lwork = _compute_lwork(trsen_lwork, select, t)

    if t.dtype in COMPLEX_DTYPES:
        result = trsen(select, t, q, lwork=lwork)
    else:
        result = trsen(select, t, q, lwork=lwork, liwork=lwork[1])
    assert_equal(result[-1], 0)

    t = result[0]
    q = result[1]
    if t.dtype in COMPLEX_DTYPES:
        s = result[4]
        sep = result[5]
    else:
        s = result[5]
        sep = result[6]

    assert_allclose(expect, q @ t @ q.conj().T, atol=atol)
    assert_allclose(expect_s, 1 / s, atol=atol2)
    assert_allclose(expect_sep, 1 / sep, atol=atol2)

