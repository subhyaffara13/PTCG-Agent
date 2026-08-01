
def test_api_date_and_index(conn, request):
    # Test case where same column appears in parse_date and index_col
    conn = request.getfixturevalue(conn)
    df = sql.read_sql_query(
        "SELECT * FROM types",
        conn,
        index_col="DateCol",
        parse_dates=["DateCol", "IntDateCol"],
    )

    assert issubclass(df.index.dtype.type, np.datetime64)
    assert issubclass(df.IntDateCol.dtype.type, np.datetime64)

