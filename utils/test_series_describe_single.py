
def test_series_describe_single():
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    grouped = ts.groupby(lambda x: x.month)
    result = grouped.apply(lambda x: x.describe())
    expected = grouped.describe().stack()
    tm.assert_series_equal(result, expected)

