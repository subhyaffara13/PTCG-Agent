
def test_closed_min_max_datetime(input_dtype, func, closed, expected):
    # see gh-21704
    ser = Series(
        data=np.arange(10).astype(input_dtype),
        index=date_range("2000", periods=10),
    )

    result = getattr(ser.rolling("3D", closed=closed), func)()
    expected = Series(expected, index=ser.index)
    tm.assert_series_equal(result, expected)

