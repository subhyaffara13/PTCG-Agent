
def test_series_describe_multikey():
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    grouped = ts.groupby([lambda x: x.year, lambda x: x.month])
    result = grouped.describe()
    tm.assert_series_equal(result["mean"], grouped.mean(), check_names=False)
    tm.assert_series_equal(result["std"], grouped.std(), check_names=False)
    tm.assert_series_equal(result["min"], grouped.min(), check_names=False)

