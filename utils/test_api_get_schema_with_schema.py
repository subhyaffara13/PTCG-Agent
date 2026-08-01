
def test_api_get_schema_with_schema(conn, request, test_frame1):
    # GH28486
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="'get_schema' not implemented for ADBC drivers",
                strict=True,
            )
        )
    conn = request.getfixturevalue(conn)
    create_sql = sql.get_schema(test_frame1, "test", con=conn, schema="pypi")
    assert "CREATE TABLE pypi." in create_sql

