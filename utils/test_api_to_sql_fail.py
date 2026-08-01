
def test_api_to_sql_fail(conn, request, test_frame1):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_frame2", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_frame2")

    sql.to_sql(test_frame1, "test_frame2", conn, if_exists="fail")
    assert sql.has_table("test_frame2", conn)

    msg = "Table 'test_frame2' already exists"
    with pytest.raises(ValueError, match=msg):
        sql.to_sql(test_frame1, "test_frame2", conn, if_exists="fail")

