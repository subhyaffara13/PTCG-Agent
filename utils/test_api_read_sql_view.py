
def test_api_read_sql_view(conn, request):
    conn = request.getfixturevalue(conn)
    iris_frame = sql.read_sql_query("SELECT * FROM iris_view", conn)
    check_iris_frame(iris_frame)

