
def test_where_empty_series_and_empty_cond_having_non_bool_dtypes():
    # https://github.com/pandas-dev/pandas/issues/34592
    ser = Series([], dtype=float)
    result = ser.where([])
    tm.assert_series_equal(result, ser)

