
def test_iloc_returns_series(indexer, expected, simple_multiindex_dataframe):
    df = simple_multiindex_dataframe
    arr = df.values
    result = indexer(df)
    expected = expected(arr)
    tm.assert_series_equal(result, expected)

