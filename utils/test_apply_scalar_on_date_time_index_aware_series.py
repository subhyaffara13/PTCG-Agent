
def test_apply_scalar_on_date_time_index_aware_series(by_row, expected):
    # GH 25959
    # Calling apply on a localized time series should not cause an error
    series = Series(
        np.arange(10, dtype=np.float64),
        index=date_range("2020-01-01", periods=10, tz="UTC"),
    )
    result = Series(series.index).apply(lambda x: 1, by_row=by_row)
    tm.assert_equal(result, expected)

