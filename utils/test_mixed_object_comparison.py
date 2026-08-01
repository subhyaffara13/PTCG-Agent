
def test_mixed_object_comparison(any_string_dtype):
    # GH#60228
    dtype = any_string_dtype
    ser = Series(["a", "b"], dtype=dtype)

    mixed = Series([1, "b"], dtype=object)

    result = ser == mixed
    expected = Series([False, True], dtype=bool)
    if dtype == object:
        pass
    elif dtype.storage == "python" and dtype.na_value is NA:
        expected = expected.astype("boolean")
    elif dtype.storage == "pyarrow" and dtype.na_value is NA:
        expected = expected.astype("bool[pyarrow]")

    tm.assert_series_equal(result, expected)

