
def test_datetime_with_timezone_query_chunksize(conn, request):
    conn = request.getfixturevalue(conn)
    expected = create_and_load_postgres_datetz(conn)

    df = concat(
        list(read_sql_query("select * from datetz", conn, chunksize=1)),
        ignore_index=True,
    )
    col = df.DateColWithTz
    tm.assert_series_equal(col, expected)

