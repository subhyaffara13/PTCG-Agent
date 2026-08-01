
def test_datetime_with_timezone_roundtrip(conn, request):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    # GH 9086
    # Write datetimetz data to a db and read it back
    # For dbs that support timestamps with timezones, should get back UTC
    # otherwise naive data should be returned
    expected = DataFrame(
        {"A": date_range("2013-01-01 09:00:00", periods=3, tz="US/Pacific", unit="us")}
    )
    assert expected.to_sql(name="test_datetime_tz", con=conn, index=False) == 3

    if "postgresql" in conn_name:
        # SQLAlchemy "timezones" (i.e. offsets) are coerced to UTC
        expected["A"] = expected["A"].dt.tz_convert("UTC")
    else:
        # Otherwise, timestamps are returned as local, naive
        expected["A"] = expected["A"].dt.tz_localize(None)

    result = sql.read_sql_table("test_datetime_tz", conn)
    tm.assert_frame_equal(result, expected)

    result = sql.read_sql_query("SELECT * FROM test_datetime_tz", conn)
    if "sqlite" in conn_name:
        # read_sql_query does not return datetime type like read_sql_table
        assert isinstance(result.loc[0, "A"], str)
        result["A"] = to_datetime(result["A"]).dt.as_unit("us")
    tm.assert_frame_equal(result, expected)

