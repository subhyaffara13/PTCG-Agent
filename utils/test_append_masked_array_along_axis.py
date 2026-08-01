
def test_append_masked_array_along_axis():
    a = np.ma.masked_equal([1, 2, 3], value=2)
    b = np.ma.masked_values([[4, 5, 6], [7, 8, 9]], 7)

    # When `axis` is specified, `values` must have the correct shape.
    assert_raises(ValueError, np.ma.append, a, b, axis=0)

    result = np.ma.append(a[np.newaxis, :], b, axis=0)
    expected = np.ma.arange(1, 10)
    expected[[1, 6]] = np.ma.masked
    expected = expected.reshape((3, 3))
    assert_array_equal(result.data, expected.data)
    assert_array_equal(result.mask, expected.mask)

