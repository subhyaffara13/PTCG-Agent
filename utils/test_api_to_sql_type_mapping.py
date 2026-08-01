
def test_api_to_sql_type_mapping(conn, request, test_frame3):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_frame5", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_frame5")

    sql.to_sql(test_frame3, "test_frame5", conn, index=False)
    result = sql.read_sql("SELECT * FROM test_frame5", conn)

    tm.assert_frame_equal(test_frame3, result)

