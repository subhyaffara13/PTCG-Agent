
def test_empty_array():
    a = empty((0, 0), dtype=complex)
    l, d, p = ldl(empty((0, 0)))
    assert_array_almost_equal(l, empty_like(a))
    assert_array_almost_equal(d, empty_like(a))
    assert_array_almost_equal(p, array([], dtype=int))

