
def test_gges_tgexc(dtype):
    rng = np.random.RandomState(1234)
    atol = np.finfo(dtype).eps*100

    n = 10
    a = generate_random_dtype_array([n, n], dtype=dtype, rng=rng)
    b = generate_random_dtype_array([n, n], dtype=dtype, rng=rng)

    gges, tgexc = get_lapack_funcs(('gges', 'tgexc'), dtype=dtype)

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

    result = tgexc(s, t, q, z, 7, 1)
    assert_equal(result[-1], 0)

    s = result[0]
    t = result[1]
    q = result[2]
    z = result[3]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(s, np.triu(s), rtol=0, atol=atol)
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(q @ s @ z.conj().T, a, rtol=0, atol=atol)
    assert_allclose(q @ t @ z.conj().T, b, rtol=0, atol=atol)

    assert_allclose(s[0, 0] / t[0, 0], d2, rtol=0, atol=atol)
    assert_allclose(s[1, 1] / t[1, 1], d1, rtol=0, atol=atol)

