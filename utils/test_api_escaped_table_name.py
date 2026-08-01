
def test_api_escaped_table_name(conn, request):
    # GH 13206
    conn_name = conn
    conn = request.getfixturevalue(conn)
    if sql.has_table("d1187b08-4943-4c8d-a7f6", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("d1187b08-4943-4c8d-a7f6")

    df = DataFrame({"A": [0, 1, 2], "B": [0.2, np.nan, 5.6]})
    df.to_sql(name="d1187b08-4943-4c8d-a7f6", con=conn, index=False)

    if "postgres" in conn_name:
        query = 'SELECT * FROM "d1187b08-4943-4c8d-a7f6"'
    else:
        query = "SELECT * FROM `d1187b08-4943-4c8d-a7f6`"
    res = sql.read_sql_query(query, conn)

    tm.assert_frame_equal(res, df)

