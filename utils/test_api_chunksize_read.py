
def test_api_chunksize_read(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(reason="chunksize argument NotImplemented with ADBC")
        )
    conn_name = conn
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_chunksize", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_chunksize")

    df = DataFrame(
        np.random.default_rng(2).standard_normal((22, 5)), columns=list("abcde")
    )
    df.to_sql(name="test_chunksize", con=conn, index=False)

    # reading the query in one time
    res1 = sql.read_sql_query("select * from test_chunksize", conn)

    # reading the query in chunks with read_sql_query
    res2 = DataFrame()
    i = 0
    sizes = [5, 5, 5, 5, 2]

    for chunk in sql.read_sql_query("select * from test_chunksize", conn, chunksize=5):
        res2 = concat([res2, chunk], ignore_index=True)
        assert len(chunk) == sizes[i]
        i += 1

    tm.assert_frame_equal(res1, res2)

    # reading the query in chunks with read_sql_query
    if conn_name == "sqlite_buildin":
        with pytest.raises(NotImplementedError, match="^$"):
            sql.read_sql_table("test_chunksize", conn, chunksize=5)
    else:
        res3 = DataFrame()
        i = 0
        sizes = [5, 5, 5, 5, 2]

        for chunk in sql.read_sql_table("test_chunksize", conn, chunksize=5):
            res3 = concat([res3, chunk], ignore_index=True)
            assert len(chunk) == sizes[i]
            i += 1

        tm.assert_frame_equal(res1, res3)

