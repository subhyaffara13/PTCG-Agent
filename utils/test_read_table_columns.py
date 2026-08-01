
def test_read_table_columns(conn, request, test_frame1):
    # test columns argument in read_table
    conn_name = conn
    if conn_name == "sqlite_buildin":
        request.applymarker(pytest.mark.xfail(reason="Not Implemented"))

    conn = request.getfixturevalue(conn)
    sql.to_sql(test_frame1, "test_frame", conn)

    cols = ["A", "B"]

    result = sql.read_sql_table("test_frame", conn, columns=cols)
    assert result.columns.tolist() == cols

