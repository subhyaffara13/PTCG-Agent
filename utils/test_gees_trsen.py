
def test_gees_trsen(dtype):
    rng = np.random.RandomState(1234)
    atol = np.finfo(dtype).eps*100

    n = 10
    a = generate_random_dtype_array([n, n], dtype=dtype, rng=rng)

    gees, trsen, trsen_lwork = get_lapack_funcs(
        ('gees', 'trsen', 'trsen_lwork'), dtype=dtype)

    result = gees(lambda x: None, a, overwrite_a=False)
    assert_equal(result[-1], 0)

    t = result[0]
    z = result[-3]

    d2 = t[6, 6]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(z @ t @ z.conj().T, a, rtol=0, atol=atol)

    select = np.zeros(n)
    select[6] = 1

    lwork = _compute_lwork(trsen_lwork, select, t)

    if dtype in COMPLEX_DTYPES:
        result = trsen(select, t, z, lwork=lwork)
    else:
        result = trsen(select, t, z, lwork=lwork, liwork=lwork[1])
    assert_equal(result[-1], 0)

    t = result[0]
    z = result[1]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(z @ t @ z.conj().T, a, rtol=0, atol=atol)

    assert_allclose(t[0, 0], d2, rtol=0, atol=atol)

