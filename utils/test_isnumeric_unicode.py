
def test_isnumeric_unicode(method, expected, any_string_dtype):
    # 0x00bc: ¼ VULGAR FRACTION ONE QUARTER
    # 0x2605: ★ not number
    # 0x1378: ፸ ETHIOPIC NUMBER SEVENTY
    # 0xFF13: ３ Em 3  # noqa: RUF003
    ser = Series(
        ["A", "3", "³", "¼", "★", "፸", "３", "four"],  # noqa: RUF001
        dtype=any_string_dtype,
    )
    expected_dtype = (
        "bool" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series(expected, dtype=expected_dtype)
    if (
        method == "isdigit"
        and isinstance(ser.dtype, StringDtype)
        and ser.dtype.storage == "pyarrow"
        and not pa_version_under21p0
    ):
        # known difference in behavior between python and pyarrow unicode handling
        # pyarrow 21+ considers ¼ and ፸ as a digit, while python does not
        expected.iloc[3] = True
        expected.iloc[5] = True

    result = getattr(ser.str, method)()
    tm.assert_series_equal(result, expected)

    # compare with standard library
    # (only for non-pyarrow storage given the above differences)
    if any_string_dtype == "object" or (
        isinstance(any_string_dtype, StringDtype)
        and any_string_dtype.storage == "python"
    ):
        expected = [getattr(item, method)() for item in ser]
        assert list(result) == expected

