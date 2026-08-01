
def test_to_datetime_cache_coerce_50_lines_outofbounds(series_length):
    # GH#45319
    ser = Series(
        [datetime.fromisoformat("1446-04-12 00:00:00+00:00")]
        + ([datetime.fromisoformat("1991-10-20 00:00:00+00:00")] * series_length),
        dtype=object,
    )
    result1 = to_datetime(ser, errors="coerce", utc=True)

    expected1 = Series([Timestamp(x) for x in ser])
    assert expected1.dtype == "M8[us, UTC]"
    tm.assert_series_equal(result1, expected1)

    result3 = to_datetime(ser, errors="raise", utc=True)
    tm.assert_series_equal(result3, expected1)

