
def test_sqlalchemy_read_table(conn, request):
    conn = request.getfixturevalue(conn)
    iris_frame = sql.read_sql_table("iris", con=conn)
    check_iris_frame(iris_frame)

