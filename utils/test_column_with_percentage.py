
def test_column_with_percentage(conn, request):
    # GH 37157
    conn_name = conn
    if conn_name == "sqlite_buildin":
        request.applymarker(pytest.mark.xfail(reason="Not Implemented"))

    conn = request.getfixturevalue(conn)
    df = DataFrame({"A": [0, 1, 2], "%_variation": [3, 4, 5]})
    df.to_sql(name="test_column_percentage", con=conn, index=False)

    res = sql.read_sql_table("test_column_percentage", conn)

    tm.assert_frame_equal(res, df)

