
def test_map_scalar_on_date_time_index_aware_series():
    # GH 25959
    # Calling map on a localized time series should not cause an error
    series = Series(
        np.arange(10, dtype=np.float64),
        index=date_range("2020-01-01", periods=10, tz="UTC"),
        name="ts",
    )
    result = Series(series.index).map(lambda x: 1)
    tm.assert_series_equal(result, Series(np.ones(len(series)), dtype="int64"))

