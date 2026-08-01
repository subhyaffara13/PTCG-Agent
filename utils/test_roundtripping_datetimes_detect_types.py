
def test_roundtripping_datetimes_detect_types(sqlite_builtin_detect_types):
    # https://github.com/pandas-dev/pandas/issues/55554
    conn = sqlite_builtin_detect_types
    df = DataFrame({"t": [datetime(2020, 12, 31, 12)]}, dtype="datetime64[ns]")
    df.to_sql("test", conn, if_exists="replace", index=False)
    result = pd.read_sql("select * from test", conn).iloc[0, 0]
    assert result == Timestamp("2020-12-31 12:00:00.000000")

