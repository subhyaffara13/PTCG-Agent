
def test_gees_trexc(dtype):
    rng = np.random.RandomState(1234)
    atol = np.finfo(dtype).eps*100

    n = 10
    a = generate_random_dtype_array([n, n], dtype=dtype, rng=rng)

    gees, trexc = get_lapack_funcs(('gees', 'trexc'), dtype=dtype)

    result = gees(lambda x: None, a, overwrite_a=False)
    assert_equal(result[-1], 0)

    t = result[0]
    z = result[-3]

    d2 = t[6, 6]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(z @ t @ z.conj().T, a, rtol=0, atol=atol)

    result = trexc(t, z, 7, 1)
    assert_equal(result[-1], 0)

    t = result[0]
    z = result[-2]

    if dtype in COMPLEX_DTYPES:
        assert_allclose(t, np.triu(t), rtol=0, atol=atol)

    assert_allclose(z @ t @ z.conj().T, a, rtol=0, atol=atol)

    assert_allclose(t[0, 0], d2, rtol=0, atol=atol)

