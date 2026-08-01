
def test_datetime_with_timezone_query(conn, request, parse_dates):
    # edge case that converts postgresql datetime with time zone types
    # to datetime64[ns,psycopg2.tz.FixedOffsetTimezone..], which is ok
    # but should be more natural, so coerce to datetime64[ns] for now
    conn = request.getfixturevalue(conn)
    expected = create_and_load_postgres_datetz(conn)

    # GH11216
    df = read_sql_query("select * from datetz", conn, parse_dates=parse_dates)
    col = df.DateColWithTz
    tm.assert_series_equal(col, expected)

