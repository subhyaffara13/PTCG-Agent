
def test_repeat(any_string_dtype):
    ser = Series(["a", "b", np.nan, "c", np.nan, "d"], dtype=any_string_dtype)

    result = ser.str.repeat(3)
    expected = Series(
        ["aaa", "bbb", np.nan, "ccc", np.nan, "ddd"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)

    result = ser.str.repeat([1, 2, 3, 4, 5, 6])
    expected = Series(
        ["a", "bb", np.nan, "cccc", np.nan, "dddddd"], dtype=any_string_dtype
    )
    tm.assert_series_equal(result, expected)


def test_repeat():
    reps = 2
    numbers = [1, 2, 3]
    names = np.array(["foo", "bar"])

    m = MultiIndex.from_product([numbers, names], names=names)
    expected = MultiIndex.from_product([numbers, names.repeat(reps)], names=names)
    tm.assert_index_equal(m.repeat(reps), expected)


def test_repeat(string_array):
    res = string_array.repeat(1000)
    # Create an empty array with expanded dimension, and fill it.  Then,
    # reshape it to the expected result.
    expected = np.empty_like(string_array, shape=string_array.shape + (1000,))
    expected[...] = string_array[:, np.newaxis]
    expected = expected.reshape(-1)

    assert_array_equal(res, expected, strict=True)

