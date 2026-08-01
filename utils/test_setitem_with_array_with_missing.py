
def test_setitem_with_array_with_missing(dtype):
    # ensure that when setting with an array of values, we don't mutate the
    # array `value` in __setitem__(self, key, value)
    arr = pd.array(["a", "b", "c"], dtype=dtype)
    value = np.array(["A", None])
    value_orig = value.copy()
    arr[[0, 1]] = value

    expected = pd.array(["A", pd.NA, "c"], dtype=dtype)
    tm.assert_extension_array_equal(arr, expected)
    tm.assert_numpy_array_equal(value, value_orig)

