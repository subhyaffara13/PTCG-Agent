
def test_read_sql_delegate(conn, request):
    if conn == "sqlite_buildin_iris":
        request.applymarker(
            pytest.mark.xfail(
                reason="sqlite_buildin connection does not implement read_sql_table"
            )
        )

    conn = request.getfixturevalue(conn)
    iris_frame1 = sql.read_sql_query("SELECT * FROM iris", conn)
    iris_frame2 = sql.read_sql("SELECT * FROM iris", conn)
    tm.assert_frame_equal(iris_frame1, iris_frame2)

    iris_frame1 = sql.read_sql_table("iris", conn)
    iris_frame2 = sql.read_sql("iris", conn)
    tm.assert_frame_equal(iris_frame1, iris_frame2)

