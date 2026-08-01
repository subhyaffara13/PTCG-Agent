
def test_api_read_sql_with_chunksize_no_result(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(reason="chunksize argument NotImplemented with ADBC")
        )
    conn = request.getfixturevalue(conn)
    query = 'SELECT * FROM iris_view WHERE "SepalLength" < 0.0'
    with_batch = sql.read_sql_query(query, conn, chunksize=5)
    without_batch = sql.read_sql_query(query, conn)
    tm.assert_frame_equal(concat(with_batch), without_batch)

