
def test_rolling_groupby_with_fixed_forward_specific(df, window_size, expected):
    # GH 43267
    indexer = FixedForwardWindowIndexer(window_size=window_size)
    result = df.groupby("a")["b"].rolling(window=indexer, min_periods=1).mean()
    tm.assert_series_equal(result, expected)

