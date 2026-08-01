
def test_one_array():
    assert OneArray() == 1
    assert OneArray().is_Integer

    oa = OneArray(3, 2, 4)
    assert oa.shape == (3, 2, 4)
    oa_e = oa.as_explicit()
    assert oa_e.shape == (3, 2, 4)

    m, n, k = symbols("m n k")
    oa = OneArray(m, n, k, 2)
    assert oa.shape == (m, n, k, 2)
    raises(ValueError, lambda: oa.as_explicit())

