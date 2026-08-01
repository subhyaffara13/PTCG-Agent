
def test_nunique_empty():
    # GH 28213
    df = DataFrame(columns=["a", "b", "c"])

    result = df.nunique()
    expected = Series(0, index=df.columns)
    tm.assert_series_equal(result, expected)

    result = df.T.nunique()
    expected = Series([], dtype=np.float64)
    tm.assert_series_equal(result, expected)

