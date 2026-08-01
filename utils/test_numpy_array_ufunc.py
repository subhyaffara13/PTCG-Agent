
def test_numpy_array_ufunc(dtype, box):
    arr = box(["a", "bb", "ccc"], dtype=dtype)

    # custom ufunc that works with string (object) input -> returning numeric
    str_len_ufunc = np.frompyfunc(lambda x: len(x), 1, 1)
    result = str_len_ufunc(arr)
    expected_cls = pd.Series if box is pd.Series else np.array
    # TODO we should infer int64 dtype here?
    expected = expected_cls([1, 2, 3], dtype=object)
    tm.assert_equal(result, expected)

    # custom ufunc returning strings
    str_multiply_ufunc = np.frompyfunc(lambda x: x * 2, 1, 1)
    result = str_multiply_ufunc(arr)
    expected = box(["aa", "bbbb", "cccccc"], dtype=dtype)
    if dtype.storage == "pyarrow":
        # TODO ArrowStringArray should also preserve the class / dtype
        if box is pd.array:
            expected = np.array(["aa", "bbbb", "cccccc"], dtype=object)
        else:
            # not specifying the dtype because the exact dtype is not yet preserved
            expected = pd.Series(["aa", "bbbb", "cccccc"])

    tm.assert_equal(result, expected)

