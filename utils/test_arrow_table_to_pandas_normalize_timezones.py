
def test_arrow_table_to_pandas_normalize_timezones():
    df = pd.DataFrame(
        {"ts": pd.date_range("2024-03-01", periods=2, tz="America/New_York")},
        index=pd.date_range("2024-01-01", periods=2, tz="US/Eastern"),
    )
    expected = df.copy()
    expected.index = expected.index._with_freq(None)

    table = pa.Table.from_pandas(df)
    result = arrow_table_to_pandas(table)

    tm.assert_frame_equal(result, expected)
    assert isinstance(result["ts"].dtype.tz, zoneinfo.ZoneInfo)
    assert isinstance(result.index.tz, zoneinfo.ZoneInfo)

