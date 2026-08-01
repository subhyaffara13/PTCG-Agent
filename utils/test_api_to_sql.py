
def test_api_to_sql(conn, request, test_frame1):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_frame1", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_frame1")

    sql.to_sql(test_frame1, "test_frame1", conn)
    assert sql.has_table("test_frame1", conn)

