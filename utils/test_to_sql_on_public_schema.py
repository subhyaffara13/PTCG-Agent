
def test_to_sql_on_public_schema(conn, request):
    if "sqlite" in conn or "mysql" in conn:
        request.applymarker(
            pytest.mark.xfail(
                reason="test for public schema only specific to postgresql"
            )
        )

    conn = request.getfixturevalue(conn)

    test_data = DataFrame([[1, 2.1, "a"], [2, 3.1, "b"]], columns=list("abc"))
    test_data.to_sql(
        name="test_public_schema",
        con=conn,
        if_exists="append",
        index=False,
        schema="public",
    )

    df_out = sql.read_sql_table("test_public_schema", conn, schema="public")
    tm.assert_frame_equal(test_data, df_out)

