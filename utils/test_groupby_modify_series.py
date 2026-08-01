
def test_groupby_modify_series():
    # https://github.com/pandas-dev/pandas/issues/63219
    # Modifying a Series after using it to groupby should not impact
    # the groupby operation.
    ser = Series([1, 2, 1])
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    gb = df.groupby(ser)
    ser.iloc[0] = 100
    result = gb.sum()
    expected = DataFrame({"a": [4, 2], "b": [10, 5]}, index=[1, 2])
    tm.assert_frame_equal(result, expected)

