
def test_reindex_fill_value_datetimelike_upcast(dtype, fill_value):
    # https://github.com/pandas-dev/pandas/issues/42921
    if dtype == "timedelta64[ns]" and fill_value == Timedelta(0):
        # use the scalar that is not compatible with the dtype for this test
        fill_value = Timestamp(0)

    ser = Series([NaT], dtype=dtype)

    result = ser.reindex([0, 1], fill_value=fill_value)
    expected = Series([NaT, fill_value], index=range(2), dtype=object)
    tm.assert_series_equal(result, expected)

