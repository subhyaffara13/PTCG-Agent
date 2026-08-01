
def test_binary_input_not_dunder():
    a = np.array([1, 2, 3])
    expected = np.array([NA, NA, NA], dtype=object)
    result = np.logaddexp(a, NA)
    tm.assert_numpy_array_equal(result, expected)

    result = np.logaddexp(NA, a)
    tm.assert_numpy_array_equal(result, expected)

    # all NA, multiple inputs
    assert np.logaddexp(NA, NA) is NA

    result = np.modf(NA, NA)
    assert len(result) == 2
    assert all(x is NA for x in result)

