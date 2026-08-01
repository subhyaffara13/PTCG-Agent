
def test_api_get_schema_dtypes(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="'get_schema' not implemented for ADBC drivers",
                strict=True,
            )
        )
    conn_name = conn
    conn = request.getfixturevalue(conn)
    float_frame = DataFrame({"a": [1.1, 1.2], "b": [2.1, 2.2]})

    if conn_name == "sqlite_buildin":
        dtype = "INTEGER"
    else:
        from sqlalchemy import Integer

        dtype = Integer
    create_sql = sql.get_schema(float_frame, "test", con=conn, dtype={"b": dtype})
    assert "CREATE" in create_sql
    assert "INTEGER" in create_sql

