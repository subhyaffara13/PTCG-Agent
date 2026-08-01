
def test_api_dtype_argument(conn, request, dtype):
    # GH10285 Add dtype argument to read_sql_query
    conn_name = conn
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_dtype_argument", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_dtype_argument")

    df = DataFrame([[1.2, 3.4], [5.6, 7.8]], columns=["A", "B"])
    assert df.to_sql(name="test_dtype_argument", con=conn) == 2

    expected = df.astype(dtype)

    if "postgres" in conn_name:
        query = 'SELECT "A", "B" FROM test_dtype_argument'
    else:
        query = "SELECT A, B FROM test_dtype_argument"
    result = sql.read_sql_query(query, con=conn, dtype=dtype)

    tm.assert_frame_equal(result, expected)

