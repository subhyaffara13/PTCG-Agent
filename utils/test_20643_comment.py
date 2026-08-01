
def test_20643_comment():
    # https://github.com/pandas-dev/pandas/issues/20643#issuecomment-431244590
    # fixed sometime prior to GH#45121
    orig = Series([0, 1, 2], index=["a", "b", "c"])
    expected = Series([np.nan, 1, 2], index=["a", "b", "c"])

    ser = orig.copy()
    ser.iat[0] = None
    tm.assert_series_equal(ser, expected)

    ser = orig.copy()
    ser.iloc[0] = None
    tm.assert_series_equal(ser, expected)

