
def test_ismethods(method, expected, any_string_dtype):
    ser = Series(
        ["A", "b", "Xy", "4", "3A", "", "TT", "55", "-", "  "], dtype=any_string_dtype
    )
    expected_dtype = (
        "bool" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series(expected, dtype=expected_dtype)
    result = getattr(ser.str, method)()
    tm.assert_series_equal(result, expected)

    # compare with standard library
    expected_stdlib = [getattr(item, method)() for item in ser]
    assert list(result) == expected_stdlib

    # with missing value
    ser.iloc[[1, 2, 3, 4]] = np.nan
    result = getattr(ser.str, method)()
    if ser.dtype == "object":
        expected = expected.astype(object)
        expected.iloc[[1, 2, 3, 4]] = np.nan
    elif ser.dtype == "str":
        # NaN propagates as False
        expected.iloc[[1, 2, 3, 4]] = False
    else:
        # nullable dtypes propagate NaN
        expected.iloc[[1, 2, 3, 4]] = np.nan

