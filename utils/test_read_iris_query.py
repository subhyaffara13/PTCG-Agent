
def test_read_iris_query(conn, request):
    conn = request.getfixturevalue(conn)
    iris_frame = read_sql_query("SELECT * FROM iris", conn)
    check_iris_frame(iris_frame)
    iris_frame = pd.read_sql("SELECT * FROM iris", conn)
    check_iris_frame(iris_frame)
    iris_frame = pd.read_sql("SELECT * FROM iris where 0=1", conn)
    assert iris_frame.shape == (0, 5)
    assert "SepalWidth" in iris_frame.columns

