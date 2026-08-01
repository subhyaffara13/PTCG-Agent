
def test_endswith_string_dtype(any_string_dtype, na):
    values = Series(
        ["om", None, "foo_nom", "nom", "bar_foo", None, "foo", "regex", "rege."],
        dtype=any_string_dtype,
    )
    result = values.str.endswith("foo", na=na)
    expected_dtype = (
        (object if na is None else bool)
        if is_object_or_nan_string_dtype(any_string_dtype)
        else "boolean"
    )
    if any_string_dtype == "str":
        # NaN propagates as False
        expected_dtype = bool
        if na is None:
            na = False
    exp = Series(
        [False, na, False, False, True, na, True, False, False], dtype=expected_dtype
    )
    tm.assert_series_equal(result, exp)

    result = values.str.endswith("rege.", na=na)
    exp = Series(
        [False, na, False, False, False, na, False, False, True], dtype=expected_dtype
    )
    tm.assert_series_equal(result, exp)

