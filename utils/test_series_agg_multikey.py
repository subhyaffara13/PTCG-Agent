
def test_series_agg_multikey():
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    grouped = ts.groupby([lambda x: x.year, lambda x: x.month])

    result = grouped.agg("sum")
    expected = grouped.sum()
    tm.assert_series_equal(result, expected)

