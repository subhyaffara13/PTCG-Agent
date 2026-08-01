
def test_roundtripping_datetimes(sqlite_engine):
    conn = sqlite_engine
    # GH#54877
    df = DataFrame({"t": [datetime(2020, 12, 31, 12)]}, dtype="datetime64[ns]")
    df.to_sql("test", conn, if_exists="replace", index=False)
    result = pd.read_sql("select * from test", conn).iloc[0, 0]
    assert result == "2020-12-31 12:00:00.000000"

