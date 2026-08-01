
def test_get_schema_create_table(conn, request, test_frame3):
    # Use a dataframe without a bool column, since MySQL converts bool to
    # TINYINT (which read_sql_table returns as an int and causes a dtype
    # mismatch)
    if conn == "sqlite_str":
        request.applymarker(
            pytest.mark.xfail(reason="test does not support sqlite_str fixture")
        )

    conn = request.getfixturevalue(conn)

    from sqlalchemy import text
    from sqlalchemy.engine import Engine

    tbl = "test_get_schema_create_table"
    create_sql = sql.get_schema(test_frame3, tbl, con=conn)
    blank_test_df = test_frame3.iloc[:0]

    create_sql = text(create_sql)
    if isinstance(conn, Engine):
        with conn.connect() as newcon:
            with newcon.begin():
                newcon.execute(create_sql)
    else:
        conn.execute(create_sql)
    returned_df = sql.read_sql_table(tbl, conn)
    tm.assert_frame_equal(returned_df, blank_test_df, check_index_type=False)

