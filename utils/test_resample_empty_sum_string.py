
def test_resample_empty_sum_string(string_dtype_no_object, min_count):
    # https://github.com/pandas-dev/pandas/issues/60229
    dtype = string_dtype_no_object
    ser = Series(
        pd.NA,
        index=DatetimeIndex(
            [
                "2000-01-01 00:00:00",
                "2000-01-01 00:00:10",
                "2000-01-01 00:00:20",
                "2000-01-01 00:00:30",
            ]
        ),
        dtype=dtype,
    )
    rs = ser.resample("20s")
    result = rs.sum(min_count=min_count)

    value = "" if min_count == 0 else pd.NA
    index = date_range(start="2000-01-01", freq="20s", periods=2, unit="us")
    expected = Series(value, index=index, dtype=dtype)
    tm.assert_series_equal(result, expected)

