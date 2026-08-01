
def test_resample_dst_midnight_last_nonexistent():
    # GH 58380
    ts = Series(
        1,
        date_range("2024-04-19", "2024-04-20", tz="Africa/Cairo", freq="15min"),
    )

    expected = Series([len(ts)], index=DatetimeIndex([ts.index[0]], freq="7D"))

    result = ts.resample("7D").sum()
    tm.assert_series_equal(result, expected)

