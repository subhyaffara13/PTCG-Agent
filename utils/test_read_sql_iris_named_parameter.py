
def test_read_sql_iris_named_parameter(conn, request, sql_strings):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="'params' not implemented for ADBC drivers",
                strict=True,
            )
        )

    conn_name = conn
    conn = request.getfixturevalue(conn)
    query = sql_strings["read_named_parameters"][flavor(conn_name)]
    params = {"name": "Iris-setosa", "length": 5.1}
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            iris_frame = pandasSQL.read_query(query, params=params)
    check_iris_frame(iris_frame)

