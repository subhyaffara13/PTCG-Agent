
def test_rolling_median_resample():
    indices = [datetime(1975, 1, i) for i in range(1, 6)]
    # So that we can have 3 datapoints on last day (4, 10, and 20)
    indices.append(datetime(1975, 1, 5, 1))
    indices.append(datetime(1975, 1, 5, 2))
    series = Series([*list(range(5)), 10, 20], index=indices)
    # Use floats instead of ints as values
    series = series.map(lambda x: float(x))
    # Sort chronologically
    series = series.sort_index()

    # Default how should be median
    expected = Series(
        [0.0, 1.0, 2.0, 3.0, 10],
        index=DatetimeIndex([datetime(1975, 1, i, 0) for i in range(1, 6)], freq="D"),
    )
    x = series.resample("D").median().rolling(window=1).median()
    tm.assert_series_equal(expected, x)

