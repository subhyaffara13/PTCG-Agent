
def test_read_table_index_col(conn, request, test_frame1):
    # test columns argument in read_table
    conn_name = conn
    if conn_name == "sqlite_buildin":
        request.applymarker(pytest.mark.xfail(reason="Not Implemented"))

    conn = request.getfixturevalue(conn)
    sql.to_sql(test_frame1, "test_frame", conn)

    result = sql.read_sql_table("test_frame", conn, index_col="index")
    assert result.index.names == ["index"]

    result = sql.read_sql_table("test_frame", conn, index_col=["A", "B"])
    assert result.index.names == ["A", "B"]

    result = sql.read_sql_table(
        "test_frame", conn, index_col=["A", "B"], columns=["C", "D"]
    )
    assert result.index.names == ["A", "B"]
    assert result.columns.tolist() == ["C", "D"]

