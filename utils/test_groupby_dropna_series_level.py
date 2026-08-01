
def test_groupby_dropna_series_level(dropna, idx, expected):
    ser = pd.Series([1, 2, 3, 3], index=idx)

    result = ser.groupby(level=0, dropna=dropna).sum()
    tm.assert_series_equal(result, expected)

