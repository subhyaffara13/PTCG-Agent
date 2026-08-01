
def test_rolling_max_resample(step):
    indices = [datetime(1975, 1, i) for i in range(1, 6)]
    # So that we can have 3 datapoints on last day (4, 10, and 20)
    indices.append(datetime(1975, 1, 5, 1))
    indices.append(datetime(1975, 1, 5, 2))
    series = Series([*list(range(5)), 10, 20], index=indices)
    # Use floats instead of ints as values
    series = series.map(lambda x: float(x))
    # Sort chronologically
    series = series.sort_index()

    # Default how should be max
    expected = Series(
        [0.0, 1.0, 2.0, 3.0, 20.0],
        index=DatetimeIndex([datetime(1975, 1, i, 0) for i in range(1, 6)], freq="D"),
    )[::step]
    x = series.resample("D").max().rolling(window=1, step=step).max()
    tm.assert_series_equal(expected, x)

    # Now specify median (10.0)
    expected = Series(
        [0.0, 1.0, 2.0, 3.0, 10.0],
        index=DatetimeIndex([datetime(1975, 1, i, 0) for i in range(1, 6)], freq="D"),
    )[::step]
    x = series.resample("D").median().rolling(window=1, step=step).max()
    tm.assert_series_equal(expected, x)

    # Now specify mean (4+10+20)/3
    v = (4.0 + 10.0 + 20.0) / 3.0
    expected = Series(
        [0.0, 1.0, 2.0, 3.0, v],
        index=DatetimeIndex([datetime(1975, 1, i, 0) for i in range(1, 6)], freq="D"),
    )[::step]
    x = series.resample("D").mean().rolling(window=1, step=step).max()
    tm.assert_series_equal(expected, x)

