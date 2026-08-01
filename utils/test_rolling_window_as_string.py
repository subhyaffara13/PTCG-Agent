
def test_rolling_window_as_string(center):
    # see gh-22590
    date_today = datetime.now()
    days = date_range(date_today, date_today + timedelta(365), freq="D")

    data = np.ones(len(days))
    df = DataFrame({"DateCol": days, "metric": data})

    df.set_index("DateCol", inplace=True)
    result = df.rolling(window="21D", min_periods=2, closed="left", center=center)[
        "metric"
    ].agg("max")

    index = days.rename("DateCol")
    index = index._with_freq(None)
    expected_data = np.ones(len(days), dtype=np.float64)
    if not center:
        expected_data[:2] = np.nan
    expected = Series(expected_data, index=index, name="metric")
    tm.assert_series_equal(result, expected)

