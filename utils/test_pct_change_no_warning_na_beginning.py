
def test_pct_change_no_warning_na_beginning():
    # GH#54981
    ser = Series([None, None, 1, 2, 3])
    result = ser.pct_change()
    expected = Series([np.nan, np.nan, np.nan, 1, 0.5])
    tm.assert_series_equal(result, expected)

