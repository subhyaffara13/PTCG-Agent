
def test_compare_tuple():
    # GH#21517
    mi = MultiIndex.from_product([[1, 2]] * 2)

    all_false = np.array([False, False, False, False])

    result = mi == mi[0]
    expected = np.array([True, False, False, False])
    tm.assert_numpy_array_equal(result, expected)

    result = mi != mi[0]
    tm.assert_numpy_array_equal(result, ~expected)

    result = mi < mi[0]
    tm.assert_numpy_array_equal(result, all_false)

    result = mi <= mi[0]
    tm.assert_numpy_array_equal(result, expected)

    result = mi > mi[0]
    tm.assert_numpy_array_equal(result, ~expected)

    result = mi >= mi[0]
    tm.assert_numpy_array_equal(result, ~all_false)

