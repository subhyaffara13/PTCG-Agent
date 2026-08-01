
def test_api_to_sql_index_label(conn, request, index_name, index_label, expected):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(reason="index_label argument NotImplemented with ADBC")
        )
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_index_label", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_index_label")

    temp_frame = DataFrame({"col1": range(4)})
    temp_frame.index.name = index_name
    query = "SELECT * FROM test_index_label"
    sql.to_sql(temp_frame, "test_index_label", conn, index_label=index_label)
    frame = sql.read_sql_query(query, conn)
    assert frame.columns[0] == expected

