
def test_with_listlike_columns():
    # GH 17348
    df = DataFrame(
        {
            "a": Series(np.random.default_rng(2).standard_normal(4)),
            "b": ["a", "list", "of", "words"],
            "ts": date_range("2016-10-01", periods=4, freq="h"),
        }
    )

    result = df[["a", "b"]].apply(tuple, axis=1)
    expected = Series([t[1:] for t in df[["a", "b"]].itertuples()])
    tm.assert_series_equal(result, expected)

    result = df[["a", "ts"]].apply(tuple, axis=1)
    expected = Series([t[1:] for t in df[["a", "ts"]].itertuples()])
    tm.assert_series_equal(result, expected)

