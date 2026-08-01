
def test_read_iris_table_chunksize(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(reason="chunksize argument NotImplemented with ADBC")
        )
    conn = request.getfixturevalue(conn)
    iris_frame = concat(read_sql_table("iris", conn, chunksize=7))
    check_iris_frame(iris_frame)
    iris_frame = concat(pd.read_sql("iris", conn, chunksize=7))
    check_iris_frame(iris_frame)

