
def test_sqlite_read_sql_delegate(sqlite_buildin_iris):
    conn = sqlite_buildin_iris
    iris_frame1 = sql.read_sql_query("SELECT * FROM iris", conn)
    iris_frame2 = sql.read_sql("SELECT * FROM iris", conn)
    tm.assert_frame_equal(iris_frame1, iris_frame2)

    msg = "Execution failed on sql 'iris': near \"iris\": syntax error"
    with pytest.raises(sql.DatabaseError, match=msg):
        sql.read_sql("iris", conn)

