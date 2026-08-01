
def test_gejsv_edge_arguments(dtype):
    """Test edge arguments return expected status"""
    gejsv = get_lapack_funcs('gejsv', dtype=dtype)

    # scalar A
    sva, u, v, work, iwork, info = gejsv(1.)
    assert_equal(info, 0)
    assert_equal(u.shape, (1, 1))
    assert_equal(v.shape, (1, 1))
    assert_equal(sva, np.array([1.], dtype=dtype))

    # 1d A
    A = np.ones((1,), dtype=dtype)
    sva, u, v, work, iwork, info = gejsv(A)
    assert_equal(info, 0)
    assert_equal(u.shape, (1, 1))
    assert_equal(v.shape, (1, 1))
    assert_equal(sva, np.array([1.], dtype=dtype))

    # 2d empty A
    A = np.ones((1, 0), dtype=dtype)
    sva, u, v, work, iwork, info = gejsv(A)
    assert_equal(info, 0)
    assert_equal(u.shape, (1, 0))
    assert_equal(v.shape, (1, 0))
    assert_equal(sva, np.array([], dtype=dtype))

    # make sure "overwrite_a" is respected - user reported in gh-13191
    A = np.sin(np.arange(100).reshape(10, 10)).astype(dtype)
    A = np.asfortranarray(A + A.T)  # make it symmetric and column major
    Ac = A.copy('A')
    _ = gejsv(A)
    assert_allclose(A, Ac)

