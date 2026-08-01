
def test_readonly_array():
    # GH-27766
    arr = np.array([1, 3, np.nan, 3, 5])
    arr.setflags(write=False)
    result = Series(arr).rolling(2).mean()
    expected = Series([np.nan, 2, np.nan, np.nan, 4])
    tm.assert_series_equal(result, expected)

