
def test_to_sql_with_negative_npinf(conn, request, input):
    # GH 34431

    df = DataFrame(input)
    conn_name = conn
    conn = request.getfixturevalue(conn)

    if "mysql" in conn_name:
        # GH 36465
        # The input {"foo": [-np.inf], "infe0": ["bar"]} does not raise any error
        # for pymysql version >= 0.10
        msg = "Execution failed on sql"
        with pytest.raises(pd.errors.DatabaseError, match=msg):
            df.to_sql(name="foobar", con=conn, index=False)
    else:
        assert df.to_sql(name="foobar", con=conn, index=False) == 1
        res = sql.read_sql_table("foobar", conn)
        tm.assert_equal(df, res)

