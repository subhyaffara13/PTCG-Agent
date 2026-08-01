
def test_sqlalchemy_read_table_columns(conn, request):
    conn = request.getfixturevalue(conn)
    iris_frame = sql.read_sql_table(
        "iris", con=conn, columns=["SepalLength", "SepalLength"]
    )
    tm.assert_index_equal(iris_frame.columns, Index(["SepalLength", "SepalLength__1"]))

