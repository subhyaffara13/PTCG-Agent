
def test_api_roundtrip(conn, request, test_frame1):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_frame_roundtrip", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_frame_roundtrip")

    sql.to_sql(test_frame1, "test_frame_roundtrip", con=conn)
    result = sql.read_sql_query("SELECT * FROM test_frame_roundtrip", con=conn)

    # HACK!
    if "adbc" in conn_name:
        result = result.drop(columns="__index_level_0__")
    else:
        result = result.drop(columns="level_0")
    tm.assert_frame_equal(result, test_frame1)

