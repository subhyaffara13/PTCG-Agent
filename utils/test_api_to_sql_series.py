
def test_api_to_sql_series(conn, request):
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_series", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_series")

    s = Series(np.arange(5, dtype="int64"), name="series")
    sql.to_sql(s, "test_series", conn, index=False)
    s2 = sql.read_sql_query("SELECT * FROM test_series", conn)
    tm.assert_frame_equal(s.to_frame(), s2)

