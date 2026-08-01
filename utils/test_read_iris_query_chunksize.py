
def test_read_iris_query_chunksize(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="'chunksize' not implemented for ADBC drivers",
                strict=True,
            )
        )
    conn = request.getfixturevalue(conn)
    iris_frame = concat(read_sql_query("SELECT * FROM iris", conn, chunksize=7))
    check_iris_frame(iris_frame)
    iris_frame = concat(pd.read_sql("SELECT * FROM iris", conn, chunksize=7))
    check_iris_frame(iris_frame)
    iris_frame = concat(pd.read_sql("SELECT * FROM iris where 0=1", conn, chunksize=7))
    assert iris_frame.shape == (0, 5)
    assert "SepalWidth" in iris_frame.columns

