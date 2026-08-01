
def test_gges_tgsen(dtype):
    rng = np.random.RandomState(1234)
    atol = np.finfo(dtype).eps*100

    n = 10
    a = generate_random_dtype_array([n, n], dtype=dtype, rng=rng)
    b = generate_random_dtype_array([n, n], dtype=dtype, rng=rng)

    gges, tgsen, tgsen_lwork = get_lapack_funcs(
        ('gges', 'tgsen', 'tgsen_lwork'), dtype=dtype)

    result = gges(lambda x: None, a, b, overwrite_a=False, overwrite_b=False)
    assert_equal(result[-1], 0)

    s = result[0]
    t = result[1]
    q = result[-4]
    z = result[-3]

    d1 = s[0, 0] / t[0, 0]
    d2 = s[6, 6] / t[6, 6]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(s, np.triu(s), rtol=0, atol=atol)
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(q @ s @ z.conj().T, a, rtol=0, atol=atol)
    assert_allclose(q @ t @ z.conj().T, b, rtol=0, atol=atol)

    select = np.zeros(n)
    select[6] = 1

    lwork = _compute_lwork(tgsen_lwork, select, s, t)

    # off-by-one error in LAPACK, see gh-issue #13397
    lwork = (lwork[0]+1, lwork[1])

    result = tgsen(select, s, t, q, z, lwork=lwork)
    assert_equal(result[-1], 0)

    s = result[0]
    t = result[1]
    q = result[-7]
    z = result[-6]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(s, np.triu(s), rtol=0, atol=atol)
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(q @ s @ z.conj().T, a, rtol=0, atol=atol)
    assert_allclose(q @ t @ z.conj().T, b, rtol=0, atol=atol)

    assert_allclose(s[0, 0] / t[0, 0], d2, rtol=0, atol=atol)
    assert_allclose(s[1, 1] / t[1, 1], d1, rtol=0, atol=atol)

