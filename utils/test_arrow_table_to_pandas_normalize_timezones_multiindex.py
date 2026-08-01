
def test_arrow_table_to_pandas_normalize_timezones_multiindex():
    df = pd.DataFrame(
        {"ts": pd.date_range("2024-03-01", periods=2, tz="America/New_York")},
        index=pd.Index([1, 2], name="index"),
    ).set_index("ts", append=True, drop=False)
    expected = df.copy()

    table = pa.Table.from_pandas(df)
    result = arrow_table_to_pandas(table)

    tm.assert_frame_equal(result, expected)
    assert isinstance(result["ts"].dtype.tz, zoneinfo.ZoneInfo)
    assert isinstance(result.index.get_level_values("ts").tz, zoneinfo.ZoneInfo)

