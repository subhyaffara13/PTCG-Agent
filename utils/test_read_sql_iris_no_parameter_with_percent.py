
def test_read_sql_iris_no_parameter_with_percent(conn, request, sql_strings):
    if "mysql" in conn or ("postgresql" in conn and "adbc" not in conn):
        request.applymarker(pytest.mark.xfail(reason="broken test"))

    conn_name = conn
    conn = request.getfixturevalue(conn)

    query = sql_strings["read_no_parameters_with_percent"][flavor(conn_name)]
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            iris_frame = pandasSQL.read_query(query, params=None)
    check_iris_frame(iris_frame)

