
def test_append_masked_array():
    a = np.ma.masked_equal([1, 2, 3], value=2)
    b = np.ma.masked_equal([4, 3, 2], value=2)

    result = np.ma.append(a, b)
    expected_data = [1, 2, 3, 4, 3, 2]
    expected_mask = [False, True, False, False, False, True]
    assert_array_equal(result.data, expected_data)
    assert_array_equal(result.mask, expected_mask)

    a = np.ma.masked_all((2, 2))
    b = np.ma.ones((3, 1))

    result = np.ma.append(a, b)
    expected_data = [1] * 3
    expected_mask = [True] * 4 + [False] * 3
    assert_array_equal(result.data[-3], expected_data)
    assert_array_equal(result.mask, expected_mask)

    result = np.ma.append(a, b, axis=None)
    assert_array_equal(result.data[-3], expected_data)
    assert_array_equal(result.mask, expected_mask)

