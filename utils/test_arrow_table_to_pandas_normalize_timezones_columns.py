
def test_arrow_table_to_pandas_normalize_timezones_columns():
    df = pd.DataFrame(
        [[1, 2], [3, 4]],
        columns=pd.date_range("2024-02-01", periods=2, tz="Europe/Berlin"),
    )
    expected = df.copy()

    table = pa.Table.from_pandas(df)
    result = arrow_table_to_pandas(table)

    if pa_version_under23p0 and not pa_version_under18p0:
        expected.columns = expected.columns.as_unit("ns")

    tm.assert_frame_equal(result, expected)
    assert isinstance(result.columns.tz, zoneinfo.ZoneInfo)

